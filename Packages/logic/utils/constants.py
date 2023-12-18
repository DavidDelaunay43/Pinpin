import os

# FUNCTIONS -------------------------------------------------------------------------------
def _generate_increment_names(tuple):
    project_subdirs = {}
    for index, subdir_name in enumerate(tuple, start=1):
        project_subdir_name = f'{index:02}_{subdir_name}'
        project_subdirs[project_subdir_name] = None
        
    return project_subdirs

def _dict_to_dirs(parent_directory, project_dict):
    
    for key, value in project_dict.items():
        
        directory_name = key
        directory_path = os.path.join(parent_directory, directory_name)
        print(f'os.mkdir({directory_path})')
        #os.mkdir(directory_path)
        
        if value:
            _dict_to_dirs(directory_path, value)

#  CONSTANTS ------------------------------------------------------------------------------
USERNAME = os.getenv('USERNAME')
PROJECT_PATH = r"E:\__Esma_pipeline\SERVEUR\Coup de Soleil"
PROJECT_NAME = os.path.basename(PROJECT_PATH)

PROJECT_SUBDIR_NAMES = (
    'ressources',
    'preprod',
    'asset',
    'texture',
    'sequence',
    'shot',
    'cache',
    'editing',
    'test',
    'com',
    'jury'
    )

ASSET_SUBDIR_NAMES = (
    'character',
    'prop',
    'item',
    'environnement',
    'module',
    'fx',
    'diorama'
)

PROJECT_SUBDIRS = _generate_increment_names(PROJECT_SUBDIR_NAMES)
ASSET_SUBDIRS = _generate_increment_names(ASSET_SUBDIR_NAMES)

PROJECT_DICT = {
    PROJECT_NAME : PROJECT_SUBDIRS
}


if __name__ == '__main__':
    import json
    print(json.dumps(PROJECT_DICT, indent=4))
    
    dir = 'E:\__Esma_pipeline\SERVEUR'
    _dict_to_dirs(dir, PROJECT_DICT)