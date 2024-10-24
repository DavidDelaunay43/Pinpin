import os
import hou
from Packages.apps.houdini.funcs.save_thumbnail import save_thumbnail
from Packages.logic.filefunc import return_increment_edit
from Packages.logic.json_funcs import set_recent_file

def increment_edit():
    '''
    '''

    current_file_path = hou.hipFile.path()
    current_file_name = os.path.basename(current_file_path)
    parent_directory = os.path.dirname(current_file_path)

    new_file_name = return_increment_edit(current_file_path)
    new_file_path = os.path.join(parent_directory, new_file_name)

    hou.hipFile.save(new_file_path)
    set_recent_file(new_file_path)

    save_thumbnail()
