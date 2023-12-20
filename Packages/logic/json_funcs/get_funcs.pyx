import os
import json
from Packages.logic.json_funcs.convert_funcs import json_to_dict
from Packages.utils.constants import (PROJECT_JSON_PATH, CLICKED_ITEMS_JSON_PATH, 
                                      CURRENT_PROJECT_DATA_FOLDER, DEV_MODE_JSON,
                                      RECENT_FILES_JSON, APPS_JSON_PATH)
from Packages.utils.logger import init_logger

logger = init_logger(__file__)

cpdef str get_pref(str app_name):
    '''
    '''
    cdef dict apps_dict = json_to_dict(APPS_JSON_PATH)
    cdef str pref = apps_dict[app_name]['pref']
    
    return pref

cpdef list get_recent_files(list ext, int length = 20):
    '''
    '''
    
    cdef dict recent_files_dict = json_to_dict(RECENT_FILES_JSON)
    cdef list recent_files_list = recent_files_dict['recent_files']
    cdef list return_list = []
    
    if ext:
        for file in recent_files_list:
            file_ext = os.path.splitext(file)[-1]
            if file_ext in ext:
                return_list.append(file)
    else:
        return_list = recent_files_list
            
    if len(return_list) > length:
        return_list = return_list[:length]
    
    return return_list

cpdef str get_current_project_name(str project_json_path):
    """
    Lit la clé du dictionnaire contenu dans 'current_project' du fichier JSON.

    Args:
        project_json_path (str): Le chemin du fichier JSON contenant 'current_project'.

    Returns:
        str: La clé du dictionnaire contenu dans 'current_project'.
    """
    with open(project_json_path, 'r') as file:
        data = json.load(file)
    
    if isinstance(data['current_project'], dict) and data['current_project']:
        key = next(iter(data['current_project']))
        return key
    else:
        return None
    
cpdef str get_current_project_path(str project_json_path):
    """Lit la valeur du dictionnaire contenu dans 'current_project' du fichier JSON.

    Args:
        project_json_path (str): Le chemin du fichier JSON contenant 'current_project'.

    Returns:
        La valeur du dictionnaire contenu dans 'current_project'.
    """
    with open(project_json_path, 'r') as file:
        data = json.load(file)
    
    if isinstance(data['current_project'], dict) and data['current_project']:
        return next(iter(data['current_project'].values()))
    else:
        return None
    
cdef str CURRENT_PROJECT_NAME = get_current_project_name(PROJECT_JSON_PATH)
cdef str CURRENT_PROJECT_PATH = get_current_project_path(PROJECT_JSON_PATH)
    
cpdef dict get_file_data(str filename):
    """
    """
    
    cdef str FILE_DATA_JSON_PATH = os.path.join(CURRENT_PROJECT_DATA_FOLDER, 'file_data.json')
    
    with open(FILE_DATA_JSON_PATH, 'r', encoding='utf-8') as json_file:
        file_data_dict = json.load(json_file)
        
    if filename in file_data_dict:
        return file_data_dict[filename]
    
    else:
        return {'comment': '', 'user': ''}

cpdef str get_clicked_radio_button():
    
    cdef dict clicked_items_dict = json_to_dict(CLICKED_ITEMS_JSON_PATH)
    return clicked_items_dict[CURRENT_PROJECT_NAME]["radio_button"]

cpdef str get_clicked_item(str radio_button, str item_index):
    
    cdef dict clicked_items_dict = json_to_dict(CLICKED_ITEMS_JSON_PATH)
    return clicked_items_dict[CURRENT_PROJECT_NAME][radio_button][item_index]

cpdef int get_dev_mode_state():
    with open(DEV_MODE_JSON, 'r') as file:
        dev_mode_data = json.load(file)

    cdef str dev_mode = dev_mode_data["dev_mode"]

    return dev_mode