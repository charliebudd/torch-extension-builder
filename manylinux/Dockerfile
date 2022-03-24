#===================================
# Docker image template for building pytorch extentions.

# The image is paramaterised by python, and cuda versions and is built on top of the 
# manylinux image "manylinux2014_x86_64" (manylinux_2_17_x86_64 in the new system)
# This manylinux specification is the minimum that PyTorch can support. 

# An alterantive approach would be to start with an nvidia cuda Image as is done here... 
# https://github.com/microsoft/onnxruntime/blob/master/tools/ci_build/github/linux/docker/Dockerfile.manylinux2014_cuda11
# The justification for this methodology is that distribution of NVIDIA CUDA Driver Libraries(libcuda.so, libnvidia-ptxjitcompiler.so) 
# is only alowed if the application is built in a docker image starting from a nvidia docker image. 
# Pytorch extentions however depend on torch and so can rely on the libraries distibuted in the torch package.

#===================================
# Starting with manylinux2014 image, CentOS7
# and lots of python versions...
FROM quay.io/pypa/manylinux2014_x86_64

#===================================
# Python, PyTorch, and CUDA version arguments, expected 
# in the form <major>.<minor>...
ARG PYTHON_VERSION
ARG PYTORCH_VERSION
ARG CUDA_VERSION

#===================================
# CUDA_ARCH_LIST and GCC_VERSION are really just dependant on the cuda 
# version, but there seems to be no easy way to conditionally set these.
# Expected values for respective cuda versions as follows...
# CUDA_VERSION  CUDA_ARCH_LIST                              GCC_VERSION          
# 10.2          3.7 5.0 6.0 6.1 6.2 7.0 7.2 7.5+PTX         8
# 11.3          3.7 5.0 6.0 6.1 6.2 7.0 7.2 7.5 8.0 8.6+PTX 10
ARG CUDA_ARCH_LIST
ARG GCC_VERSION

#===================================
# Installing required cuda version...
RUN yum-config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/cuda-rhel7.repo; \
    yum clean all; \
    yum --enablerepo=epel -y install cuda-${CUDA_VERSION//./-}; \
    yes | rm /opt/nvidia/nsight-* /usr/local/cuda/samples /usr/local/cuda/libnvvp /usr/local/cuda/nsightee_plugins -r; \
    yum clean all;

#===================================
# Setting up correct gcc version for nvcc...
RUN yum -y install zip devtoolset-${GCC_VERSION}-toolchain; \
    ln -sf /opt/rh/devtoolset-${GCC_VERSION}/root/usr/bin/gcc /usr/local/cuda/bin/gcc; \
    ln -sf /opt/rh/devtoolset-${GCC_VERSION}/root/usr/bin/g++ /usr/local/cuda/bin/g++; \
    yum clean all;

#===================================
# Setting up python environment...
RUN ln -sf python${PYTHON_VERSION} /usr/local/bin/python; \
    ln -sf $(ls /opt/_internal/cpython-${PYTHON_VERSION}.* -d) /opt/_internal/cpython-${PYTHON_VERSION}; \
    python -m pip install --upgrade pip; \
    python -m pip --no-cache-dir install setuptools ninja numpy wheel; \
    export FULL_PYTORCH_VERSION=$(python -m pip index versions torch -f https://download.pytorch.org/whl/torch_stable.html | grep -o ${PYTORCH_VERSION}.[0-9]+cu${CUDA_VERSION//.} | head -n 1); \
    python -m pip --no-cache-dir install torch==${FULL_PYTORCH_VERSION} -f https://download.pytorch.org/whl/torch_stable.html;

#===================================
# Setting environment variables...
ENV PYTHON_VERSION "${PYTHON_VERSION}"
ENV PYTORCH_VERSION "${PYTORCH_VERSION}"
ENV CUDA_VERSION "${CUDA_VERSION}"
ENV TORCH_CUDA_ARCH_LIST "${CUDA_ARCH_LIST}"
ENV TORCH_LIBRARY_PATH "/opt/_internal/cpython-${PYTHON_VERSION}/lib/python${PYTHON_VERSION}/site-packages/torch/lib"
ENV LD_LIBRARY_PATH "${TORCH_LIBRARY_PATH}:$LD_LIBRARY_PATH"

#===================================
# Adding scripts...
ADD scripts /torch_extention_builder
