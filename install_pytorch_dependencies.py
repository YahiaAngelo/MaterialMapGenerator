import os
import sys
import subprocess


def install_pytorch_modules():
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", "torch", "torchvision", "--extra-index-url", "https://download.pytorch.org/whl/cu116", "--upgrade", "--user"], check=True, env=environ_copy)


def install_pytorch_amd_modules():
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", "torch", "torchvision", "--extra-index-url", "https://download.pytorch.org/whl/rocm5.2/", "--upgrade", "--user"], check=True, env=environ_copy)

