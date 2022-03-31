# Torch Extension Builder (WIP)
A build system for generating (relatively) lightweight and portable PyPI wheels containing PyTorch C++/CUDA extensions. Wheels built with Torch Extension Builder dynamically link to the Torch and CUDA libraries included with the users PyTorch installation. No CUDA instalation is required on the end users machine.

## Target System Support
Packages built using Torch Extension Builder currently suppport the following runtime environments...

<div>
<img src="https://img.shields.io/badge/OS-Linux%20(glibc%20>=%202.17)-7a3b8f.svg"/>
<img src="https://img.shields.io/badge/Python-3.6%20|%203.7%20|%203.8%20|%203.9-3776ab.svg"/>
<br />
<img src="https://img.shields.io/badge/PyTorch-1.9%20|%201.10%20|%201.11-EE4C2C.svg"/>
<img src="https://img.shields.io/badge/CUDA-10.2%20|%2011.3-76b900.svg"/>
<div />

## Explanation
Torch extensions are tricky to deploy via PyPI. Source distributions require the user to have the CUDA Toolkit installed, the version of which must match the users PyTorch installation. Binary wheels on the other hand must link to the versions of the Torch and CUDA libraries available at compilation time. Bundling these libraries with the wheel creates wheels much larger then the PyPI wheel size limit. It also creates a clumsy user experience as a package for each PyTorch and CUDA version combination must be created. This means the user must specify the correct cuda and pytorch version when installing, for example ```pip install my_neat_package``` would become ```pip install my_neat_package_pt110_cu113```. 

Torch Extension Builder overcomes these problems in two main steps. Firstly, dependancies which are included with PyTorch are stripped from the wheel, and the extension instead links to the instances of these libraries which are included with the users PyTorch installation. This reduces the size of the wheels significantly. Secondly, with the size of the wheels reduced, multiple compilations of the extension can be included in each wheel. The correct compilation is then determined at runtime based on the users PyTorch installation.
  
## Usage
The example workflow below illustrates an automated release system using Torch Extension Builder to build the PyPI wheels. 

The first job `build-wheels` calls the workflow `build-pytorch-extension-wheels` which is hosted in this repository. This will produce a wheel for each python versions provided as arguments. Each wheel will support systems with any of the PyTorch and CUDA versions also provided as arguments. The resulting wheels will be cached in a github artifact named `final-wheels`. 

The second job `publish-wheels`, which is set to run once `build-wheels` has finished, will then download the cached wheels and publish them to TestPyPI.

```
name: Example Build Workflow

on:
  push:
    branches:
      - main

jobs:

  build-wheels:
    name: Build Wheels Using Torch Extension Builder
    uses: charliebudd/torch-extension-builder/.github/workflows/build-pytorch-extension-wheels.yml@main
    with:
        python-versions: "[3.6, 3.7, 3.8]"
        pytorch-versions: "[1.9, '1.10']"
        cuda-versions: "[10.2, 11.3]"

  publish-wheels:
    name: Publish Wheels To TestPyPI
    runs-on: ubuntu-latest
    needs: build-wheels
    steps:
      - name: Download Cached Wheels
        uses: actions/download-artifact@v3
        with:
          name: final-wheels
          path: dist

      - name: Publish Package to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.TEST_PYPI_API_TOKEN }}
          repository_url: https://test.pypi.org/legacy/
```
