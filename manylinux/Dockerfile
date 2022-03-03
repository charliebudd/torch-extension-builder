#===================================
# Starting with manylinux2014 image. 
# CentOS 7, lots of python versions...
FROM quay.io/pypa/manylinux2014_x86_64

#===================================
# Installing required cuda versions...
RUN yum-config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/cuda-rhel7.repo
RUN yum clean all
RUN yum --enablerepo=epel -y install cuda-10-2 cuda-11-3

#===================================
# Setting up python environments
RUN for PY in "3.6" "3.7" "3.8"; do \
        for CU in "102" "113"; do \
            python$PY -m venv pyenvs/py$PY-cu$CU; \
            pyenvs/py$PY-cu$CU/bin/python -m pip install torch==1.10.2+cu$CU -f https://download.pytorch.org/whl/cu$CU/torch_stable.html; \
        done; \
    done
