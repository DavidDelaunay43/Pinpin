import hou
from Packages.utils.funcs import forward_slash
from Packages.logic.json_funcs import set_recent_file

def open_houdini_file(file_path: str):
    '''
    '''
    
    file_path = forward_slash(file_path)
    hou.hipFile.load(file_path)
    set_recent_file(file_path)
