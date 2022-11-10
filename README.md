# Material Map Generator

  
A Blender plugin to easily generate Material Maps from an Image Texture with one click using [Material-Map_generator](https://github.com/joeyballentine/Material-Map-Generator) by [Joey Ballentine](https://github.com/joeyballentine).

## Requirments:
* System: Windows/Linux/MacOs
* GPU: 
	1. Nvidia GPU with a [CUDA-capable](https://developer.nvidia.com/cuda-zone) system 
	2. AMD GPU with an [ROCm-capable](https://rocmdocs.amd.com/en/latest/Installation_Guide/Installation_new.html) system (Linux only) 
	3. Apple M1 chip
* Blender version: 2.91.0+

## Installation:
1. Download MaterialMapGenerator.zip from the [lateset release](https://github.com/YahiaAngelo/MaterialMapGenerator/releases/latest).
2. Open Blender prefrences -> Add-ons -> Install and choose the downloaded package.
3. Enable the plugin then click on: 
* "Install dependencies" if you have an Nvida GPU.
* "Install AMD GPU dependencies" if you have an AMD GPU.
* "Install Apple M1 dependencies" if you have an Apple M1 machine.
4. Go grab some coffee because the previous step will take some time (Pro tip: Click on window -> Toggle system console to see the progress).

## Usage:

1. Go to your shader editor and click on your Image Texture node with an image then click on "node" menu and choose "Generate Material Maps".
2. Wait for a couple of seconds and Boom! you have Material Maps!
![Preview1](https://github.com/YahiaAngelo/MaterialMapGenerator/blob/master/preview/preview1.png?raw=true)
