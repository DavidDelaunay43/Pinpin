import os
import re
import datetime
import shutil
import subprocess
from functools import partial

_OS_DICT = {'dir': os.path.isdir, 'file': os.path.isfile}

def _get_items(directory_path: str, type: str) -> dict:
    """
    """
    
    item_names = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if _OS_DICT[type](item_path):
            item_names.append(item)
            
    return sorted(item_names)

get_dirs = partial(_get_items, type = 'dir')
get_files = partial(_get_items, type = 'file')

def clean_directory(path: str, dir: str):
    """
    """
    
    return path if dir not in path else path.split(dir)[0]

def get_version_file(version: str, parent_directory: str):
    
    for file in get_files(parent_directory):
        if version in file:
            return file
        
def get_version_num(filename: str):
    match = re.search(r'\d{3}', filename)

    # Si une suite de trois chiffres est trouvée, la renvoyer
    if match:
        return match.group()

    # Sinon, renvoyer une chaîne vide
    return ""
    
def get_file_modification_date_time(file_name):
    try:
        # Obtenir les informations de modification du fichier
        file_stat = os.stat(file_name)

        # Convertir le timestamp de modification en objet datetime
        modification_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)

        # Formater la date et l'heure selon le format demandé (par exemple, "27/08/2023 16:28")
        formatted_date_time = modification_time.strftime("%d/%m/%Y %H:%M")

        return formatted_date_time
    except FileNotFoundError:
        return None  # Le fichier n'existe pas
    except Exception as e:
        return str(e)  # Gérer toute autre exception

def open_explorer(path: str):
    
    path = path.replace('/', '\\')
    subprocess.Popen(['explorer', path])

def return_publish_name(file_name: str):
    '''Renomme un fichier en remplaçant la partie "_E_" suivie de chiffres par "_P".

    Parameters:
        file_name (str): Le nom du fichier à renommer.

    Returns:
        str: Le nouveau nom de fichier avec la partie correspondante modifiée.
    '''
    
    edit_string = r'_E_\d+'
    match = re.findall(edit_string, file_name)[0]
    publish_file_name = file_name.replace(match, '_P')
    
    return publish_file_name

def extract_increment(file_name: str):
    
    edit_string = r'_E_\d+'
    match = re.search(edit_string, file_name).group()
    print(match)
    if not match: return
    
    increment_string = re.search(r'\d+', match).group()
    return int(increment_string)

def return_increment_edit(file_path: str):
    
    parent_dir = os.path.dirname(file_path)
    other_files = get_files(parent_dir)
    last_file = sorted(other_files)[-1]
    last_increment = extract_increment(last_file)
    
    new_increment = f'_E_{last_increment + 1:03}'
    
    edit_string = r'_E_\d+'
    match = re.findall(edit_string, file_path)[0]
    
    return file_path.replace(match, new_increment)

def increment_file_external(file_path: str):
    '''
    '''
    
    parent_directory = os.path.dirname(file_path)
    new_file_name = return_increment_edit(file_path)
    new_file_path = os.path.join(parent_directory, new_file_name)
    print(new_file_path)
    print(parent_directory)
    shutil.copy(file_path, new_file_path)
    return new_file_path
    