import os
import glob
import zipfile
import hashlib
import base64
import argparse
from distutils import dir_util
from subprocess import check_output

IMPORT_WRAPPER_HEADER = '''
from torch import __version__

def __get_version_code__():
    torch_version = "".join(__version__.split(".")[:2])
    cuda_version = __version__.split("+cu")[-1]
    return "pt" + torch_version + "cu" + cuda_version

__version_code__ = __get_version_code__()
'''

IMPORT_WRAPPER_CASE = '''
if __version_code__ == "{1}":
    from {1}.{0} import *
'''

def wrap_libraries(wheel_dir):
    all_libraries = glob.glob(f"{wheel_dir}/*.so.*")
    library_names = list(set([lib.split("/")[-1].split(".")[0] for lib in all_libraries]))
    for library_name in library_names:
        wrapper_file_text = IMPORT_WRAPPER_HEADER.format(library_name)
        for library in glob.glob(f"{wheel_dir}/{library_name}*.so*"):
            library_code = library.split(".so.")[-1]
            new_library_file = library.replace(library_name, library_code + "/" + library_name)
            new_library_file = new_library_file.split(".so")[0] + ".so"
            os.makedirs(os.path.dirname(new_library_file))
            os.rename(library, new_library_file)
            libs_dir = glob.glob(wheel_dir + "/*.libs")[0].split("/")[-1]
            check_output(["patchelf", "--set-rpath", f"$ORIGIN/../torch/lib:$ORIGIN/../{libs_dir}", f"{new_library_file}"])
            wrapper_file_text += IMPORT_WRAPPER_CASE.format(library_name, library_code)
        with open(wheel_dir + "/" + library_name + ".py", "w") as f:
            f.write(wrapper_file_text)

def write_recrord_file(wheel_dir):
    
    def get_file_hash(file):
        with open(file, 'rb') as f:
            file_data = f.read()
        hash_code = hashlib.sha256(file_data).digest()
        safe_hash_code = base64.urlsafe_b64encode(hash_code).decode('latin1').rstrip('=')
        return safe_hash_code

    def get_word_count(file):
        word_count = int(check_output(["wc", "-c", file]).split()[0])
        return word_count

    record_file = glob.glob(f"{wheel_dir}/*/RECORD")[0]
    
    with open(record_file, 'w') as f:
        for (dirpath, _, filenames) in os.walk(wheel_dir):
            for file in [f"{dirpath}/{file}" for file in filenames]:
                relative_path = os.path.relpath(file, wheel_dir)
                if file != record_file:
                    hash = get_file_hash(file)
                    wc = get_word_count(file)
                    f.write(f"{relative_path},sha256={hash},{wc}\n")
                else:
                    f.write(f"{relative_path},,\n")

def combine_wheel(wheels):
    
    print("Combining wheels...")
    map(print, wheels)

    wheel_name = wheels[0].split("/")[-1].split(".whl.")[0]
    dir_util.mkpath(wheel_name)

    for wheel in wheels:

        wheel_tag = wheel.split(".whl.")[-1]

        with zipfile.ZipFile(wheel, 'r') as zip:
            zip.extractall(wheel_tag)

        for library in glob.glob(f"{wheel_tag}/*.so"):
            os.rename(library, f"{library}.{wheel_tag}")
        
        dir_util.copy_tree(wheel_tag, wheel_name)

        dir_util.remove_tree(wheel_tag)
    
    wrap_libraries(wheel_name)

    write_recrord_file(wheel_name)

    dir_util.mkpath("final_wheels")
    with zipfile.ZipFile("final_wheels/" + wheel_name + ".whl", 'w') as zip:
        for (dirpath, _, filenames) in os.walk(wheel_name):
            for file in [f"{dirpath}/{file}" for file in filenames]:
                arc_name = "/".join(file.split("/")[1:])
                zip.write(file, arc_name)

    dir_util.remove_tree(wheel_name)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Combine wheel files comompiled with different versions of PyTorch and CUDA.')
    parser.add_argument('wheels', type=str, nargs='+', help='The wheel files to be combined.')
    args = parser.parse_args()

    combine_wheel(args.wheels)
