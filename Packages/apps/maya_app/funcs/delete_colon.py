import sys
from Packages.apps.maya_app.funcs import debug_funcs

def run_delete_colon(publish_file_directory):
    shading_nodes = debug_funcs.list_shading_nodes()
    debug_funcs.delete_colon(publish_file_directory, shading_nodes)


publish_file_directory = sys.argv[1]
print(f'PYTHON W - publish_file_directory : {publish_file_directory}')
run_delete_colon(publish_file_directory)
