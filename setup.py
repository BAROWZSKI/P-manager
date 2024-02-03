import importlib
import subprocess
import sys

def install_and_check(library_name):
    try:
        # checks if library already exist
        importlib.import_module(library_name)
        print(f"{library_name} already installed.")
    except ImportError:
        python_exe = sys.executable
        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", library_name])
            print(f"{library_name} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {library_name}: {e}")

if __name__ == "__main__":
    libraries_to_install = ["colorama", "urllib", "base64", "os.path", "json", "random"]
    for library in libraries_to_install:
        install_and_check(library)