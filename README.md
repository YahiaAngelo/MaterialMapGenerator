# Material Map Generator

  
A Blender plugin to easily generate Material Maps from an Image Texture with one click using [Material-Map_generator](https://github.com/joeyballentine/Material-Map-Generator) by [Joey Ballentine](https://github.com/joeyballentine).

## Requirments:
* System: Windows/Linux
* GPU: Nvidia GPU with a [CUDA-capable](https://developer.nvidia.com/cuda-zone) system or an AMD GPU with a [ROCm-capable](https://rocmdocs.amd.com/en/latest/Installation_Guide/Installation_new.html) system (Linux only)
* Blender version: 2.9.1+

## Installation:
1. Download the [lateset release](https://github.com/YahiaAngelo/MaterialMapGenerator/releases/latest).
2. If you're using Windows, open Blender as adminstrator.
3. Open Blender prefrences -> Add-ons -> Install and choose the downloaded package.
4. Enable the plugin then click on "Install dependencies" if you have an Nvida GPU or "Install AMD GPU dependencies" if you have an AMD GPU.

## Usage:

1. Go to your shader editor and click on your Image Texture node with an image then click on "node" menu and choose "Generate Material Maps".
2. Wait for a couple of seconds and Boom! you have Material Maps!
![Preview1](https://github.com/YahiaAngelo/MaterialMapGenerator/blob/master/preview/preview1.png?raw=true)
