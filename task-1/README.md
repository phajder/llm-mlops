# Task 1 - LLM deployment on k3s

## K3s configuration with Ansible
1. Bootstrap k3s with ansible playbook.
    ```bash
    ansible-playbook playbooks/site.yml -i inventory.yaml
    ```
2. Setup k3s default runtime to nvidia. 
    ```bash
    sudo cp /var/lib/rancher/k3s/agent/etc/containerd/config.toml /var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl
    sudo sed -i '/\[plugins."io.containerd.grpc.v1.cri".containerd\]/a \ \ default_runtime_name = "nvidia"' /var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl
    ```
3. Install [k8s-device-plugin](https://github.com/NVIDIA/k8s-device-plugin). [GPU operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/overview.html) for more complex environments (which internally uses gpu device plugin).
    ```bash
    kubectl create -k .
    ```
4. Sanity check.
    ```bash
    kubectl apply -f k8s-device-plugin-test.yaml
    kubectl logs nbody-gpu-benchmark
    ```

## Prepare container image for llama2-7B with llama-cpp-python
Model: https://huggingface.co/TheBloke/Llama-2-7B-GGUF/blob/main/llama-2-7b.Q4_K_M.gguf
Used [llama-cpp-python](https://github.com/abetlen/llama-cpp-python), based on [llama.cpp](https://github.com/ggerganov/llama.cpp) for serving due to insufficient VRAM.

1. Separate OS and [python dependencies](/llama-cpp/requirements.txt) between build and runtime stages.
2. Create [Dockerfile](/llama-cpp/Dockerfile) with separate build and runtime stages. Changed one from [cuda simple example](https://github.com/abetlen/llama-cpp-python/blob/main/docker/cuda_simple/Dockerfile)
3. Build and push (credentials obtained) container image to [DockerHub repo](https://hub.docker.com/r/phajder/llama-cpp-ph).
    ```bash
    docker build -t phajder/llama-cpp-ph:0.1-cuda .
    docker push phajder/llama-cpp-ph:0.1-cuda
    ```
    **Disclaimer**: for simplicity, only CUDA version of the image was build. Thus, usage of this image may not be valid for machines without gpu support due to missing libcuda.so mapping from nvidia-container-toolkit.
4. Test in local docker conditions:
    ```bash
    docker run --rm --gpus all -v ~/models/llama:/app/models llama-cpp-ph:0.1-cuda python3 main.py
    ```
    _Note: in volume mapping definition it was assumed that OS supports path sustitutions (~, $)._

## Handle model data in k8s
1. If not deployed automatically during k3s setup, deploy [local-path-provisioner](https://github.com/rancher/local-path-provisioner).
2. Fetch model on each k8s node.
    ```bash
    mkdir -p ~/models/llama-2-7b-quantized
    wget -P ~/models/llama-2-7b-quantized https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf
    ```
    Path can be basically anything if k8s have sufficient (chmod) permissions. In the solution, home directory was used.
3. Specify mapping for the pod in descriptor:
    ```yaml
    spec:
      ...
      containers:
        - name: llama-server
        ...
        volumeMounts:
          - name: models
            mountPath: /app/models
            readOnly: true
        ...
      volumes:
        - name: models
          hostPath:
            path: /home/phajder/models/llama-2-7b-quantized
    ```
    
    This approach was selected because model must be served locally. However, it is still possible to use this model by multiple pods on the same Node if its specification allows it:
    * GPU mode, with MIG profiles or gpu time-slicing (not recommended)
    * CPU mode, with sufficient memory on Node

    In more complex environments, [NFS mounts](https://kubernetes.io/docs/concepts/storage/storage-classes/#nfs) can be utilized to share models across Nodes (or straighlty as k8s volume if networking performance is of secondary matter).
4. Create ansible role to download specified models during cluster bootstrap.

## Deploy llama2 in k8s
1. Create new helm chart
    ```bash
    helm create llama-serve
    ```
2. Modify content to create [pod](llama-serve/templates/pod.yaml), [svc](llama-serve/templates/service.yaml), and [ingress](llama-serve/templates/ingress.yaml).
3. Specify required [values](llama-serve/values.yaml).
4. Install chart in cluster in separate namespace.
    ```bash
    helm install --create-namespace --namespace llama-serve chat ./llama-serve
    ```

## Model testing

1. Using ingress enabled:
    ```bash
    curl -X 'POST' \
      'http://cherry.lan/v1/completions' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "prompt": "\n\n### Instructions:\nWhat is the capital of Spain?\n\n### Response:\n",
      "stop": [
        "\n",
        "###"
      ]
    }'
    ```
2. With port forwarding:
    ```bash
    kubectl port-forward -n llama-serve services/chat-llama-serve 8080:8080
    curl -X 'POST' \
      'http://localhost:8080/v1/completions' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "prompt": "\n\n### Instructions:\nWhat is the capital of France?\n\n### Response:\n",
      "stop": [
        "\n",
        "###"
      ]
    }'
    ```

## Cleanup
```bash
helm uninstall --namespace llama-serve chat
kubectl delete namespaces llama-serve
```
