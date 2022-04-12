FROM mcr.microsoft.com/windows/servercore:ltsc2022

SHELL ["cmd", "/S", "/C"]

#===================================
# Installing msvc...
RUN curl -k -L https://aka.ms/vs/17/release/vs_buildtools.exe --output vs_buildtools.exe & \
    vs_buildtools.exe --quiet --wait --norestart --nocache \
        --installPath "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools" \
        --add Microsoft.VisualStudio.Workload.AzureBuildTools \
        --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 \
        --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 \
        --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 \
        --remove Microsoft.VisualStudio.Component.Windows81SDK & \
    del /q vs_buildtools.exe

#===================================
# Installing required cuda version...
ARG CUDA_VERSION="10.2"
ARG CUDA_URL="https://developer.download.nvidia.com/compute/cuda/$CUDA_VERSION/Prod/local_installers"
ARG CUDA_FILE="cuda_$CUDA_VERSION.89_441.22_win10.exe"

RUN curl -k -L "%CUDA_URL%/%CUDA_FILE%" --output "%CUDA_FILE%" & \
    %CUDA_FILE% -s nvcc_%CUDA_VERSION% & \
    setx path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin;%path%" & \
    del -f "%CUDA_FILE%"

#===================================
# Setting up python...

ARG PYTHON_VERSION="3.9"
ADD install-python.bat /
RUN install-python.bat %PYTHON_VERSION%

#===================================
# Setting up python environment...
ARG PYTORCH_VERSION="1.9"

RUN python -m pip --no-cache-dir install --upgrade pip & \
    python -m pip --no-cache-dir install setuptools ninja numpy wheel & \
    python -m pip --no-cache-dir install torch==%PYTORCH_VERSION%.0+cu%CUDA_VERSION:.=% -f https://download.pytorch.org/whl/torch_stable.html
