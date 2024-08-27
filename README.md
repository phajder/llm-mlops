# MLOps task

## Environment specification
For this task, virtual machine based on qemu was created.

* Arch: amd64
* 8 cores (2x4), Intel Xeon Silver 4214 @ 2.20 GHz
* 32 GB DDR4 memory, ECC, without balooning due to PCIe passthrough
* Nvidia RTX 2080ti (Gigabyte 11GB GDDR6), PCIe passthrough
* NIC bridged (actively) to bond of 2x 1Gbps links
* Kernel: linux 6.1.0-23
* Distro: Debian bookworm 12.2.0-14

## Prerequisites
It was assumed that this type of environment is only for dev/test purposes and some security aspects are of secondary matter. In a production and fully virtualized environment I would use cloud-init for configuration. Also, using cloud images in PVE require more bootstraping at the beginning which are irrelevant for this task due to differences in qemu storage format.

For access machine, following steps were performed.
1. Installed [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) for interacting with k3s cluster.
2. Installed [ansible](https://formulae.brew.sh/formula/ansible) for cluster bootstraping. Starting repo: [k3s-ansible](https://github.com/k3s-io/k3s-ansible).

For k3s node:
1. Manually installed debian bookwork.
2. Basic OS setup: potential upgrades of the OS and additional software: sudo, python3, python3-apt, gcc, vim, git, curl, wget, gnupg, nfs-common. I also installed zsh and set it as default shell because of my personal preference.
3. Installed [nvidia open driver](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html) and [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) for GPU usage in k3s. Also, installed cuda-drivers-fabricmanager and nvidia-container-runtime, according to [k3s docs](https://docs.k3s.io/advanced?_highlight=containerd#nvidia-container-runtime-support).
4. Set up passwordless login using PKI (ed25519).
    ```bash
    ssh-keygen -t ed25519 -f $HOME/.ssh/cherry-k3s
    ssh-copy-id -i .ssh/cherry-k3s cherry.lan
    ```
    SSH config:
    ```
    Host cherry.lan
        Hostname cherry.lan
        User phajder
        IdentityFile ~/.ssh/cherry-k3s
    ```
5. Converted this image to PVE template, in case of further extensions or any critical errors during any setup inside VM.
6. Created full clone from template and setup the VM with local DNS server. Assigned domains: cherry.local.retrolab.phd (FQDN), cherry.lan (local access).

## Tasks

| No. |                         Description                        |
| :-: | :--------------------------------------------------------- |
|  1  | [LLM deployment](/task-1/README.md) |
|  2  | [LLM pipeline with Argo Workflows](https://github.com/phajder/llama-argocd/blob/da661fe63ada0718a007c72c10de326fe3ed9c7e/README.md) |
|  3  | [Project decisions](/task-3/README.md) |

## Links

1. For server-grade GPUs, [MIG](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-operator-mig.html) can be used.
2. Problem with nvidia-container-toolkit on k3s - https://github.com/NVIDIA/k8s-device-plugin/issues/406#issuecomment-1831551692.
3. Text generation web ui helm - https://github.com/handyman5/text-generation-webui-helm.

### llama3
1. https://llama.meta.com/docs/llama-everywhere/running-meta-llama-on-linux/
2. https://github.com/meta-llama/llama3
3. https://github.com/pytorch/serve/tree/master/examples/large_models/inferentia2/llama/continuous_batching
4. https://pytorch.org/blog/high-performance-llama/

### Torch serve k8s
1. https://pytorch.org/serve/custom_service.html
2. https://github.com/pytorch/serve/tree/master/kubernetes


