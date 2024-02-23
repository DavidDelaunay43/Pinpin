import sys
from Packages.apps.maya_app.funcs.debug_funcs import delete_colon
from Packages.apps.maya_app.funcs.debug_funcs import list_shading_nodes

def run_delete_colon(publish_file_directory):
    shading_nodes = list_shading_nodes()
    delete_colon(publish_file_directory, shading_nodes)


publish_file_directory = sys.argv[1]
print(f'PYTHON W - publish_file_directory : {publish_file_directory}')
run_delete_colon(publish_file_directory)
