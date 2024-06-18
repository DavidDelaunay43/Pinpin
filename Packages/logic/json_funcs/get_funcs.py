import os
import json
from Packages.logic.json_funcs import convert_funcs
from Packages.utils.constants import (PROJECT_JSON_PATH, CLICKED_ITEMS_JSON_PATH, 
                                      CURRENT_PROJECT_DATA_FOLDER, DEV_MODE_JSON,
                                      RECENT_FILES_JSON, APPS_JSON_PATH)
from Packages.utils.logger import init_logger

logger = init_logger(__file__)


def get_pref(app_name: str) -> str:
    '''
    '''

    # récupérer le répertoire de préférences dans le .json
    apps_dict: dict = convert_funcs.json_to_dict(APPS_JSON_PATH)
    pref: str = apps_dict[app_name]['pref']
    
    return pref


def get_recent_files(ext: list = [], length: int = 20) -> list:
    '''
    '''
    
    # récupérer la liste des fichiers récents dans le .json
    recent_files_dict: dict = convert_funcs.json_to_dict(RECENT_FILES_JSON)
    recent_files_list: list = recent_files_dict['recent_files']
    return_list: list = []
    
    # filtrer les fichiers qui ont la même extension passée dans l'argument "ext"
    if ext:
        for file in recent_files_list:
            file_ext = os.path.splitext(file)[-1]
            if file_ext in ext:
                return_list.append(file)
    else:
        return_list = recent_files_list

    # garder le nombre de fichiers spécifié par l'argument "length"      
    if len(return_list) > length:
        return_list = return_list[:length]
    
    return return_list


def get_current_project_name(project_json_path: str) -> str:
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


def get_current_project_path(project_json_path: str):
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


CURRENT_PROJECT_NAME = get_current_project_name(PROJECT_JSON_PATH)
CURRENT_PROJECT_PATH = get_current_project_path(PROJECT_JSON_PATH)


def get_file_data(filename: str) -> dict:
    """
    """
    
    FILE_DATA_JSON_PATH: str = os.path.join(CURRENT_PROJECT_DATA_FOLDER, 'file_data.json')
    
    with open(FILE_DATA_JSON_PATH, 'r', encoding='utf-8') as json_file:
        file_data_dict: dict = json.load(json_file)
        
    if filename in file_data_dict:
        return file_data_dict[filename]
    
    else:
        return {'comment': '', 'user': ''}


def get_clicked_radio_button() -> str:
    
    clicked_items_dict: dict = convert_funcs.json_to_dict(CLICKED_ITEMS_JSON_PATH)
    return clicked_items_dict[CURRENT_PROJECT_NAME]["radio_button"]


def get_clicked_item(radio_button: str, item_index: str) -> str:
    
    clicked_items_dict: dict = convert_funcs.json_to_dict(CLICKED_ITEMS_JSON_PATH)
    return clicked_items_dict[CURRENT_PROJECT_NAME][radio_button][item_index]


def get_clicked_items(radio_button: str):

    all_clicked_items_dict: dict = convert_funcs.json_to_dict(CLICKED_ITEMS_JSON_PATH)
    return all_clicked_items_dict[radio_button]


def get_dev_mode_state() -> int:
    with open(DEV_MODE_JSON, 'r') as file:
        dev_mode_data = json.load(file)

    return dev_mode_data["dev_mode"]
