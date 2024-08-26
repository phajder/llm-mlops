ARG CUDA_DEV_IMAGE="12.6.0-devel-ubuntu22.04"
ARG CUDA_RUN_IMAGE="12.6.0-runtime-ubuntu22.04"

FROM nvidia/cuda:${CUDA_DEV_IMAGE} AS builder
WORKDIR /app
RUN mkdir -p /app/build

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential \
    python3 python3-pip gcc wget \
    ocl-icd-opencl-dev opencl-headers clinfo \
    libclblast-dev libopenblas-dev \
    && apt-get -y clean \
    && mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

# setting build related env vars
ENV CUDA_DOCKER_ARCH=all
ENV GGML_CUDA=1

# Install depencencies
RUN python3 -m pip install --upgrade pip pytest cmake scikit-build setuptools

# Install llama-cpp-python (build with cuda)
RUN CMAKE_ARGS="-DGGML_CUDA=on" pip install --target /app/build llama-cpp-python


FROM nvidia/cuda:${CUDA_RUN_IMAGE} AS serving
WORKDIR /app

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3 python3-pip \
    && apt-get -y clean

# Copy python packages built in the previous stage
# PYTHONPATH env can be used for consistency
# More: https://stackoverflow.com/questions/2915471/install-a-python-package-into-a-different-directory-using-pip
# In normal situations build and runtime environments are much easier to maintain, e.g. torch-serve, tensorflow-serving, fully managed python/cpp api project
COPY --from=builder /app/build/ /usr/local/lib/python3.10/dist-packages

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run the server
CMD [ "python3" "-m" "llama_cpp.server" ]
