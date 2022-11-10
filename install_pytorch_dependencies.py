import os
import sys
import subprocess


def install_pytorch_modules(target):
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", "torch", "torchvision", "--extra-index-url", "https://download.pytorch.org/whl/cu116", "--no-cache-dir", "--target", target], check=True, env=environ_copy)


def install_pytorch_amd_modules(target):
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", "torch", "torchvision", "--extra-index-url", "https://download.pytorch.org/whl/rocm5.2/", "--no-cache-dir", "--target", target], check=True, env=environ_copy)


def install_pytorch_apple_modules(target):
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", "torch", "torchvision", "--extra-index-url", "https://download.pytorch.org/whl/nightly/cpu", "--no-cache-dir", "--target", target], check=True, env=environ_copy)
