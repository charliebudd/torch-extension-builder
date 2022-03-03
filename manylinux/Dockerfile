#===================================
# Starting with manylinux2014 image, CentOS7
# and lots of python versions...
FROM quay.io/pypa/manylinux2014_x86_64

#===================================
# Python and cuda version arguments, expected 
# in the form <major>.<minor>...
ARG PYTHON_VERSION
ARG CUDA_VERSION

#===================================
# Installing required cuda version...
RUN yum-config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/cuda-rhel7.repo; \
    yum clean all; \
    yum --enablerepo=epel -y install cuda-${CUDA_VERSION//./-}

#===================================
# Setting up python environment...

RUN ln -sf python${PYTHON_VERSION} /usr/local/bin/python; \
    python -m pip install setuptools ninja wheel; \
    python -m pip install torch==1.10.2+cu${CUDA_VERSION//.} -f https://download.pytorch.org/whl/cu${CUDA_VERSION//.}/torch_stable.html
