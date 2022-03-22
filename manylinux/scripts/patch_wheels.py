import os
import glob
import shutil
import argparse

import torch
import utils

def strip_mangling(library_file):
    base_name = os.path.basename(library_file)
    name = base_name.split("-")[0].split(".so")[0]
    version = base_name.split(".so")[-1]
    return ".so".join([name, version])

def get_dependancy_substitutes(wheel_dependancies, torch_libraries):
    substitutes = []
    for dependancy in wheel_dependancies:
        for library in torch_libraries:
            if strip_mangling(dependancy) == strip_mangling(library):
                substitutes.append((dependancy, library))
    return substitutes

def patch_wheel(wheel_path, output_dir="patched_wheels"):
    
    # Parsing info from wheel path...
    wheel_file = os.path.basename(wheel_path)
    wheel_name = os.path.splitext(wheel_file)[0]
    package_name, package_version = wheel_name.split("-")[:2]
    package_id = "-".join([package_name, package_version])

    # Directories
    work_dir = package_id
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Unpack wheel into temporary directory...
    utils.unpack_wheel(wheel_path)

    # Finding libraries and dependancies...
    wheel_libraries = glob.glob(f"{work_dir}/*.so")
    wheel_dependancies = glob.glob(f"{work_dir}/{package_name}.libs/*.so*")
    torch_libraries = glob.glob(os.path.join(os.path.dirname(torch.__file__), "lib", "*.so*"))

    # Make substitutions and remove duplicate library...
    substitutes = get_dependancy_substitutes(wheel_dependancies, torch_libraries)

    print("Redirecting dependancies...")
    for original_library, new_library in substitutes:
        original_library_name = os.path.basename(original_library)
        new_library_name = os.path.basename(new_library)
        print(original_library_name, "->", new_library_name)
        for wheel_library in wheel_libraries:
            utils.replace_dependancy(wheel_library, original_library_name, new_library_name)
        os.remove(original_library)

    # Add torch/lib path to rpath...
    for wheel_library in wheel_libraries:
        utils.write_rpath(wheel_library, f"$ORIGIN/{package_name}.libs:$ORIGIN/torch/lib")

    # Repack wheel and remove temporary directory...
    utils.pack_wheel(work_dir, output_dir)
    patched_wheel = glob.glob(f"{output_dir}/*.whl")[0]
    os.rename(patched_wheel, f"{patched_wheel}.{utils.get_ptcu_code()}")
    shutil.rmtree(work_dir)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Patches a built wheel to reference the libraries included in an assumed pytorch install')
    parser.add_argument('wheel', type=str, help='The wheel file to patch.')
    args = parser.parse_args()

    patch_wheel(args.wheel)
