import os
import json
from Packages.logic.json_funcs.convert_funcs import json_to_dict, dict_to_json
from Packages.logic.json_funcs.get_funcs import CURRENT_PROJECT_NAME
from Packages.utils.funcs import forward_slash
from Packages.utils.constants import (PROJECT_JSON_PATH, CLICKED_ITEMS_JSON_PATH, FILE_DATA_JSON_PATH,
                                      RECENT_FILES_JSON, USERNAME)
from Packages.utils.logger import init_logger

logger = init_logger(__file__)

def set_recent_file(file_path: str):
    '''
    '''
    
    # récupérer la liste des fichiers récents dans le .json
    recent_files_dict = json_to_dict(RECENT_FILES_JSON)
    recent_files_list = recent_files_dict['recent_files']
    
    # si le fichier est déjà dans la liste, le placer au début de la liste
    if file_path in recent_files_list:
        recent_files_list.remove(file_path)
    recent_files_list.insert(0, file_path)
    
    # mettre à jour la liste et l'envoyer dans le .json
    recent_files_dict['recent_files'] = recent_files_list
    dict_to_json(recent_files_dict, RECENT_FILES_JSON)


def set_current_project(project_path: str) -> str:
    """Met à jour le projet actuel dans un fichier JSON avec le chemin du nouveau projet.

    Args:
        project_path (str): Le chemin absolu du nouveau projet.

    Returns:
        str: Le nom du projet mis à jour.
    """
    
    project_name = os.path.basename(project_path)
    
    with open(PROJECT_JSON_PATH, 'r') as file:
        project_dict = json.load(file)
    
    project_dict['current_project'] = {project_name: project_path}
    project_dict['projects'][project_name] = project_path

    with open(PROJECT_JSON_PATH, 'w') as file:
        json.dump(project_dict, file, indent=4)
        
    return project_name

def set_clicked_radio_button(radio_button):
    
    # vérifier si l'argument passé est bien une string
    if not isinstance(radio_button, str) and radio_button:
        radio_button = radio_button.text()
    
    # passer le radio button dans la clé "radio_button" du .json
    clicked_items_dict = json_to_dict(CLICKED_ITEMS_JSON_PATH)
    clicked_items_dict[CURRENT_PROJECT_NAME]["radio_button"] = radio_button
    dict_to_json(clicked_items_dict, CLICKED_ITEMS_JSON_PATH)


def set_clicked_item(radio_button, item_index, item, shot=False, item_parent=None):
    
    # vérifier si l'argument passé est bien une string
    if not isinstance(radio_button, str) and radio_button:
        radio_button = radio_button.text()
        
    if not isinstance(item, str) and item:
        item = item.text()

    # condition shot -> à patcher 
    if shot:
        clicked_items_dict = json_to_dict(CLICKED_ITEMS_JSON_PATH)
        clicked_items_dict[CURRENT_PROJECT_NAME][radio_button][item_index] = [item, item_parent]
        dict_to_json(clicked_items_dict, CLICKED_ITEMS_JSON_PATH)
        return
    
    # envoyer les informations dans le .json
    clicked_items_dict = json_to_dict(CLICKED_ITEMS_JSON_PATH)
    clicked_items_dict[CURRENT_PROJECT_NAME][radio_button][item_index] = item
    dict_to_json(clicked_items_dict, CLICKED_ITEMS_JSON_PATH)


def update_file_data(file_path: str, comment_string: str = '') -> None:
    '''
    '''
    
    file_path = forward_slash(file_path)
    file_infos_dict = json_to_dict(FILE_DATA_JSON_PATH)
    
    if not file_path in file_infos_dict.keys():
        file_infos_dict[file_path] = {'comment': None, 'user': None}
        
    file_infos_dict[file_path]['user'] = USERNAME
    
    # vérifier s'il y a du texte dans la "comment_string"
    if bool(comment_string.strip()):
        file_infos_dict[file_path]['comment'] = comment_string
        
    dict_to_json(file_infos_dict, FILE_DATA_JSON_PATH)
    
    logger.info(f'Update file data :\n comment: {comment_string}\n user : {USERNAME}')
