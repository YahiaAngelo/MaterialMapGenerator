import os, bpy, shutil

def absolute_path(component):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), component)

def path_iterator(folder_path):
    for fp in os.listdir(folder_path):
        if fp.endswith( tuple( bpy.path.extensions_image ) ):
            yield fp

def delete_files_in_path(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))