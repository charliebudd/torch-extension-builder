from setuptools import setup
from torch.utils import cpp_extension

setup(
    name="torchextensiontest",
    ext_modules=[cpp_extension.CUDAExtension("torchextensiontest", ["torchextensiontest/extension.cu"])],
    cmdclass={"build_ext": cpp_extension.BuildExtension}
)
