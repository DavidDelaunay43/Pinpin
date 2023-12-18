import os
import shutil
from Packages.utils.constants import WORKSPACE_MEL_PATH, EMPTY_MAYA_MA_PATH, EMPTY_NUKE_PATH, EMPTY_HOUDINI_NC_PATH, EMPTY_HOUDINI_PATH

def create_project(directory: str, parent_directory_name: str, sub_directories: list):
    """
    """
    
    parent_directory_path = os.path.join(directory, parent_directory_name)
    os.mkdir(parent_directory_path)
    
    for sub_directory_name in sub_directories:
        
        sub_directory_path = os.path.join(parent_directory_path, sub_directory_name)
        os.mkdir(sub_directory_path)

    if parent_directory_name == 'maya':
        shutil.copy(WORKSPACE_MEL_PATH, parent_directory_path)

def create_houdini_project(directory: str, departments: list, sub_directories: list, empty_scenes: bool = False):
    """
    """
    
    create_project(directory, 'houdini', sub_directories)
    scenes_directory_path = os.path.join(os.path.join(directory, 'houdini'), 'scenes')
    
    # Edit
    edit_directory_path = os.path.join(scenes_directory_path, 'edit')
    os.mkdir(edit_directory_path)
    
    for department_name in departments:
        department_path = os.path.join(edit_directory_path, department_name)
        os.mkdir(department_path)
        
        if empty_scenes:
            shutil.copy(EMPTY_HOUDINI_NC_PATH, department_path)
    
    # Publish
    publish_old_path = os.path.join(scenes_directory_path, 'publish', 'OLD')
    os.makedirs(publish_old_path)

def create_maya_project(directory: str, departments: list, sub_directories: list, empty_scenes: bool = False):
    """
    """
    
    create_project(directory, 'maya', sub_directories)
    scenes_directory_path = os.path.join(os.path.join(directory, 'maya'), 'scenes')
    
    # Edit
    edit_directory_path = os.path.join(scenes_directory_path, 'edit')
    os.mkdir(edit_directory_path)
    
    for department_name in departments:
        department_path = os.path.join(edit_directory_path, department_name)
        os.mkdir(department_path)
        
        if empty_scenes:
            shutil.copy(EMPTY_MAYA_MA_PATH, department_path)
    
    # Publish
    publish_old_path = os.path.join(scenes_directory_path, 'publish', 'OLD')
    os.makedirs(publish_old_path)
    
    # workspace.mel
    maya_directory_path = os.path.join(directory, 'maya')
    shutil.copy(WORKSPACE_MEL_PATH, maya_directory_path)
    
def create_nuke_project(directory: str, empty_scene: bool = False):
    """
    """
    
    nuke_directory_path = os.path.join(directory, 'nuke')
    input_directory_path = os.path.join(nuke_directory_path, 'input')
    output_directory_path = os.path.join(nuke_directory_path, 'output')
    os.path.mkdir(nuke_directory_path)
    os.path.mkdir(input_directory_path)
    os.path.mkdir(output_directory_path)
    
    if empty_scene:
        shutil.copy(EMPTY_NUKE_PATH, nuke_directory_path)
        
def rename_empty_scene(empty_scene_path: str, new_name: str):
    """
    """
    
    current_directory = os.path.dirname(empty_scene_path)
    empty_scene_name = os.path.basename(empty_scene_path)
    empty_scene_name_no_ext, ext = os.path.splitext(empty_scene_name)
    
    # TO DO
    
    new_name = f'{empty_scene_name_no_ext}{ext}'
    new_name_path = os.path.join(current_directory, new_name)
    os.rename(empty_scene_path, new_name_path)