from setuptools import setup
from torch.utils import cpp_extension

setup(
    name="torchextentiontest",
    ext_modules=[cpp_extension.CUDAExtension("torchextentiontest", ["torchextentiontest/extention.cu"])],
    cmdclass={"build_ext": cpp_extension.BuildExtension}
)
