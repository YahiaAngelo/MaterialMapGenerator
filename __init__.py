bl_info = {
    "name": "Material Map Generator",
    "author": "YahiaAngelo",
    "version": (1, 0, 0),
    "blender": (2, 91, 0),
    "location": "Shader Editor > node > Generate Material Maps",
    "description": "Extracts Material Maps from Image Textures",
    "warning": "Requires installation of dependencies",
    "tracker_url": "https://github.com/YahiaAngelo/MaterialMapGenerator/issues",
    "support": "COMMUNITY",
    "category": "Shader Editor"}


import bpy
from .absolute_path import absolute_path, path_iterator, delete_files_in_path
from .install_dependencies import install_pip, install_and_import_module
from .install_pytorch_dependencies import install_pytorch_modules, install_pytorch_amd_modules
import os
import subprocess
import shutil
from collections import namedtuple

def main(operator, context):
    space = context.space_data
    node_tree = space.node_tree
    node_active = context.active_node
    node_selected = context.selected_nodes

    # now we have the context, perform a simple operation
    if node_active in node_selected:
        node_selected.remove(node_active)
    if len(node_selected) > 1:
        operator.report({'ERROR'}, "1 node must be selected")
        return

    if node_active.name != 'Image Texture':
        operator.report({'ERROR'}, "Please select an Image Texture")
        return
    
    if node_active.image.filepath == "":
        operator.report({'ERROR'}, "Please add an image")
        return
    #Copy the image from ImageTexture to plugin input folder
    shutil.copy2(node_active.image.filepath, absolute_path("input"))

    from .generate import GenerateMaterialMap
    generate = GenerateMaterialMap()
    generate.start()
    
    images = []
    originalPath = os.path.dirname(node_active.image.filepath)
    for imgPath in path_iterator(absolute_path("output")):
        fullPath = os.path.join(absolute_path("output"), imgPath)
        shutil.copy2(fullPath, originalPath)
        newImage = bpy.data.images.load(os.path.join(originalPath, imgPath))
        images.append(newImage)

    new_nodes = []
    for image in images:
        node_new = node_tree.nodes.new(node_active.bl_idname)
        for key, input in enumerate(node_active.inputs):
            node_new.inputs[key].default_value = input.default_value
        node_new.image = image
        new_nodes.append(node_new)

    #Delete all images processed
    delete_files_in_path(absolute_path("input"))
    delete_files_in_path(absolute_path("output"))

    return new_nodes



class NodeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.material_mapper"
    bl_label = "Generate Material Maps"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):
        main(self, context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(NodeOperator.bl_idname, text=NodeOperator.bl_label)


Dependency = namedtuple("Dependency", ["module", "package", "name"])

# Declare all modules that this add-on depends on, that may need to be installed. The package and (global) name can be
# set to None, if they are equal to the module name. See import_module and ensure_and_import_module for the explanation
# of the arguments. DO NOT use this to import other parts of your Python add-on, import them as usual with an
# "import" statement.
dependencies = (Dependency(module="numpy", package=None, name=None),
                Dependency(module="opencv-python", package=None, name=None),)

dependencies_installed = False

class InstallDependenciesOT(bpy.types.Operator):
    bl_idname = "material_mapper.install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                      "Internet connection is required. Blender may have to be started with "
                      "elevated permissions in order to install the package")
    bl_options = {"REGISTER", "INTERNAL"}

    #@classmethod
    #def poll(self, context):
    #   # Deactivate when dependencies have been installed
    #   return not dependencies_installed

    def execute(self, context):
        try:
            install_pip()
            for dependency in dependencies:
                install_and_import_module(module_name=dependency.module,
                                          package_name=dependency.package,
                                          global_name=dependency.name)
            install_pytorch_modules()
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = True

        return {"FINISHED"}

class InstallAmdDependenciesOT(bpy.types.Operator):
    bl_idname = "material_mapper.install_amd_dependencies"
    bl_label = "Install AMD GPU dependencies"
    bl_description = ("Please click on this instead if you have an AMD GPU (Linux only)")
    bl_options = {"REGISTER", "INTERNAL"}

    #@classmethod
    #def poll(self, context):
    #   # Deactivate when dependencies have been installed
    #   return not dependencies_installed

    def execute(self, context):
        try:
            install_pip()
            for dependency in dependencies:
                install_and_import_module(module_name=dependency.module,
                                          package_name=dependency.package,
                                          global_name=dependency.name)
            install_pytorch_amd_modules()
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = True

        return {"FINISHED"}


class Prefrences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator(InstallDependenciesOT.bl_idname, icon="CONSOLE")
        layout.operator(InstallAmdDependenciesOT.bl_idname, icon="CONSOLE")



preference_classes = (InstallDependenciesOT,
                      InstallAmdDependenciesOT,
                      Prefrences)


def register():
    for cls in preference_classes:
        bpy.utils.register_class(cls)

    bpy.utils.register_class(NodeOperator)
    bpy.types.NODE_MT_node.append(menu_func)


def unregister():
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)

    bpy.utils.unregister_class(NodeOperator)
    bpy.types.NODE_MT_node.remove(menu_func)


if __name__ == "__main__":
    register()
