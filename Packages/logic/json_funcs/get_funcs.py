import os
import json
from Packages.logic.json_funcs import convert_funcs
from Packages.utils.constants.project_pinpin_data import pinpin_data_FILE_DATA, CURRENT_PROJECT_NAME
from Packages.utils.constants.preferences import CLICKED_ITEMS_JSON_PATH, RECENT_FILES_JSON_PATH, APPS_JSON_PATH, UI_PREFS_JSON_PATH


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
    recent_files_dict: dict = convert_funcs.json_to_dict(RECENT_FILES_JSON_PATH)
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


def get_file_data(filename: str) -> dict:
    """
    """
    
    with open(pinpin_data_FILE_DATA, 'r', encoding='utf-8') as json_file:
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
    with open(UI_PREFS_JSON_PATH, 'r') as file:
        ui_prefs_data = json.load(file)

    return ui_prefs_data["dev_mode"]
