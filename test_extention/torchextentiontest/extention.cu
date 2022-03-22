#include <cuda_runtime.h>
#include <torch/extension.h>

std::string get_info()
{
    int cuda_version_code; cudaRuntimeGetVersion(&cuda_version_code);
    std::string cuda_major_version = std::to_string(cuda_version_code / 1000);
    std::string cuda_minor_version = std::to_string((cuda_version_code % 1000) / 10);
    std::string cuda_version_info = "Cuda Version: " + std::to_string(cuda_version_code);
    // std::string cuda_version_info = "Cuda Version: " + cuda_major_version + "." + cuda_minor_version;

    std::string torch_major_version = std::to_string(TORCH_VERSION_MAJOR);
    std::string torch_minor_version = std::to_string(TORCH_VERSION_MINOR);
    std::string torch_patch_version = std::to_string(TORCH_VERSION_PATCH);
    std::string torch_version_info = "Torch Version: " + torch_major_version + "." + torch_minor_version + "." + torch_patch_version;

    return cuda_version_info + "\n" + torch_version_info;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) 
{
    m.def("get_info", &get_info);
}
