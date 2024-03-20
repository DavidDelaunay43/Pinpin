import os
from Packages.logic.filefunc.file_class import AssetFileInfos, SequenceFileInfos, ShotFileInfos
from Packages.utils.constants import PUBLISH_DIR

NAMING_DICT = {
    'chr': '01_character',
    'prp': '02_prop',
    'itm': '03_item',
    'env': '04_enviro',
    'mod': '05_module',
    'drm': '06_diorama',
    'masterLayout': '01_master_layout',
    'masterCamera': '02_master_camera',
    'masterLighting': '03_master_lighting'
}

def return_value(input_key: str, dico: dict):

    if input_key in dico:
        return dico[input_key]
    
    for key in dico.keys():
        if key.lower() in input_key.lower():
            return dico[key]

def find_base_directory(file_path: str):

    dir_names = ('asset', 'sequence', 'shot')

    for dir in dir_names:
        if dir in file_path:
            return dir

def find_publish_directory(file_path: str):

    file_name = os.path.basename(file_path)
    base_folder = find_base_directory(file_path)
    asset_publish_directory = None

    if base_folder == 'asset':

        file_infos = AssetFileInfos(file_name)
        asset_type_folder = NAMING_DICT[file_infos.ASSET_TYPE]
        asset_department_folder = file_infos.DEPARTMENT
        asset_publish_directory = os.path.join(PUBLISH_DIR, base_folder, asset_type_folder, asset_department_folder)
        # 09_publish/asset/01_character/geo/

    elif base_folder == 'sequence':

        file_infos = SequenceFileInfos(file_name)
        sequence_num_folder = file_infos.SEQUENCE
        #sequence_department_folder = NAMING_DICT[file_infos.DEPARTMENT] old
        sequence_department_folder = return_value(file_infos.DEPARTMENT, NAMING_DICT)
        asset_publish_directory = os.path.join(PUBLISH_DIR, base_folder, sequence_num_folder, sequence_department_folder)
        # 09_publish/sequence/seq010/01_master_layout/

    elif base_folder == 'shot':

        file_infos = ShotFileInfos(file_name)
        sequence_num_folder = file_infos.SEQUENCE
        shot_num_folder = file_infos.SHOT
        asset_publish_directory = os.path.join(PUBLISH_DIR, base_folder, sequence_num_folder, shot_num_folder)
        # 09_publish/shot/seq010/sh010/

    else:
        print('ERROR') # temporaire

    return asset_publish_directory
