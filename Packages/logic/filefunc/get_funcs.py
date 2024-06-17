import os
import re
import datetime
import operator
from typing import Literal
from Packages.logic.filefunc.file_class import AssetFileInfos, SequenceFileInfos, ShotFileInfos


def get_items(directory_path: str, type: Literal['dir', 'file'], exclude_type: list = []) -> list:
    """
    Retourne une liste triée des noms d'éléments (fichiers ou répertoires) dans le chemin spécifié.

    Args:
    - directory_path (str): Chemin du répertoire où chercher les éléments.
    - type (str): Type d'éléments à rechercher ('dir' pour répertoires, 'file' pour fichiers).
    - exclude_type (list, optional): Liste des extensions à exclure pour les fichiers. Par défaut, vide.

    Returns:
    - list: Liste triée des noms des éléments correspondants aux critères spécifiés.
    """
    
    os_dict = {
        'dir': os.path.isdir, 
        'file': os.path.isfile
    }
    
    if type not in ['dir', 'file']:
        raise ValueError("Le paramètre 'type' doit être soit 'dir' soit 'file'.")
    
    item_names = []
    for item in os.listdir(directory_path):

        item_path = os.path.join(directory_path, item)

        if item.endswith(tuple(exclude_type)):
            continue

        if os_dict[type](item_path):
            item_names.append(item)
            
    return sorted(item_names)


def get_dirs(directory_path: str):
    print(f'Search directories in directory : {directory_path}')
    return get_items(directory_path=directory_path, type='dir')
    

def get_files(directory_path: str):
    print(f'Search files in directory : {directory_path}')
    return get_items(directory_path=directory_path, type='file', exclude_type = [".txt", '.mel', '.db'])


def get_version_file(version: str, parent_directory: str):
    """
    Renvoie le nom du fichier contenant la version spécifiée dans le répertoire parent.

    Args:
    - version (str): Version recherchée dans le nom du fichier.
    - parent_directory (str): Chemin du répertoire parent où rechercher le fichier.

    Returns:
    - str: Nom du fichier contenant la version spécifiée.
    """
    
    for file in get_files(parent_directory):
        if version in file:
            return file

       
def get_file_base_folder(filename: str):
    '''
    '''
    
    if '_seq' in filename:
        if '_sh' in filename:
            return 'shot'
        return 'sequence'
    
    else:
        return 'asset'
    
    
def get_version_num(filename: str):
    '''Récupère un numéro de version à trois chiffres à partir du nom de fichier spécifié.

    Args :
    filename (str) : Le nom de fichier à partir duquel le numéro de version doit être extrait.

    Returns :
    str : Le numéro de version à trois chiffres extrait du nom de fichier, ou une chaîne vide si aucun numéro de version n'est trouvé.
    '''
    
    if '_E_' in filename:
        
        match = re.search(r'\d{3}', filename[::-1])

        # Si une suite de trois chiffres est trouvée, la renvoyer
        if match:
            return match.group(0)[::-1]

        # Sinon, renvoyer une chaîne vide
        return ""
    
    elif '_P_' in filename:
        
        match = re.search(r'\d{3}', filename)

        # Si une suite de trois chiffres est trouvée, la renvoyer
        if not match:
            return ''
        
        increment =  match.group()
        
        base_folder = get_file_base_folder(filename)
        
        if base_folder == 'asset':
            infos = AssetFileInfos(filename)
            name = infos.asset_name()
        
        elif base_folder == 'sequence':
            infos = SequenceFileInfos(filename)
            name = infos.sequence()
            
        else:
            infos = ShotFileInfos(filename)
            name = infos.shot()
            
        return f'{name}\n{increment}'
        
    
    elif '_P.' in filename:
        base_folder = get_file_base_folder(filename)
        
        if base_folder == 'asset':
            infos = AssetFileInfos(filename)
            name = infos.asset_name()
        
        elif base_folder == 'sequence':
            infos = SequenceFileInfos(filename)
            name = infos.sequence()
            
        else:
            infos = ShotFileInfos(filename)
            name = infos.shot()
        
        return name
    
    else:
        return ''


def get_file_modification_date_time(file_path: str):
    '''Récupère la date et l'heure de modification d'un fichier spécifié au format "jj/mm/aaaa hh:mm".

    Args :
    file_path (str) : Le chemin du fichier dont la date de modification doit être récupérée.

    Returns :
    str : La date et l'heure de modification du fichier au format "jj/mm/aaaa hh:mm", ou None si le fichier n'existe pas.
    '''
    
    if not os.path.exists(file_path):
        return
    
    # Obtenir les informations de modification du fichier
    file_stat = os.stat(file_path)

    # Convertir le timestamp de modification en objet datetime
    modification_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)

    # Formater la date et l'heure selon le format demandé (par exemple, "27/08/2023 16:28")
    formatted_date_time = modification_time.strftime("%d/%m/%Y %H:%M")
    
    formatted_date = modification_time.strftime("%d/%m/%Y")
    formatted_time = modification_time.strftime("%H:%M")
    
    formatted_date_time = f'{formatted_date}\n{formatted_time}'

    return formatted_date_time
    

def return_publish_name(file_name: str, usd: bool = False, variant: str = ''):
    '''Renomme un fichier en remplaçant la partie "_E_" suivie de chiffres par "_P".

    Parameters:
        file_name (str): Le nom du fichier à renommer.

    Returns:
        str: Le nouveau nom de fichier avec la partie correspondante modifiée.
    '''
    
    edit_string = r'_E_\d+'
    match = re.findall(edit_string, file_name)[0]
    publish_file_name = file_name.replace(match, '_P')
    
    if usd:
        base_name = os.path.splitext(publish_file_name)[0]
        publish_file_name = f'{base_name}.usd'
    
    dirname = os.path.dirname(publish_file_name)
    base_name = os.path.basename(publish_file_name)
    # CDS_chr_petru_ldv_P.ma
    if get_file_base_folder(base_name) == 'asset':
        
        pfx, asset_type, asset_name, dep, end = base_name.split('_')
        asset_name = f'{asset_name}{variant}'
        base_name = '_'.join([pfx, asset_type, asset_name, dep, end])
        
        publish_file_name = os.path.join(dirname, base_name)
    
    print(f'Return Publish Name : {publish_file_name}')
    return publish_file_name


def extract_increment(file_name: str, mode = 'E'):
    '''Extrait l'incrément numérique d'un nom de fichier contenant un suffixe "_E_" suivi d'un nombre.

    Args :
    file_name (str) : Le nom de fichier à partir duquel l'incrément doit être extrait.

    Returns :
    int : L'incrément numérique extrait du nom de fichier, ou None si aucun incrément n'est trouvé.
    '''
    
    edit_string = fr'_{mode}_\d+'
    match = re.search(edit_string, file_name).group()
    print(match)
    if not match: return
    
    increment_string = re.search(r'\d+', match).group()
    return int(increment_string)


def return_increment_edit(file_path: str):
    '''Modifie le nom de fichier en ajoutant un suffixe numérique incrémenté "_E_" à la fin du nom
    pour indiquer une édition. Le nouvel increment est basé sur les fichiers existants dans le
    répertoire parent.

    Args :
    file_path (str) : Le chemin du fichier dont le nom doit être modifié.

    Returns :
    str : Le chemin du fichier avec le nouveau nom incrémenté.
    '''
    
    parent_dir = os.path.dirname(file_path)
    other_files = get_files(parent_dir)
    last_file = sorted(other_files)[-1]
    last_increment = extract_increment(last_file)
    
    new_increment = f'_E_{last_increment + 1:03}'
    
    edit_string = r'_E_\d+'
    match = re.findall(edit_string, file_path)[0]
    
    return file_path.replace(match, new_increment)


def return_increment_publish_name(file_name: str, publish_list: list):
    
    if not publish_list:
        return file_name.replace('.', f'_001.')

    publish_list.sort()
    last_publish_file = publish_list[-1]
    new_increment = f'{extract_increment(last_publish_file, mode="P") + 1:03}'

    new_last_publish_file_name = file_name.replace('.', f'_{new_increment}.')

    return new_last_publish_file_name


def clean_directory(path: str, dir: str):
    """
    """
    print('Clean Directory')
    print(f'Path : {path}')
    print(f'Path : {path}')
    
    if dir not in path:
        return path
    
    else:
        return path.split(dir)[0]


def _get_files_by_extension(directory: str):
    '''
    '''
    
    EXTENSIONS = ('.ma', '.mb', '.hip', '.hipnc', '.nk', '.zpr')
    
    return_dict = {}
    
    for root_directory, _, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(EXTENSIONS)):
                file_path = os.path.join(root_directory, file)
                date_time = datetime.datetime.fromtimestamp(os.stat(file_path).st_mtime)
                
                return_dict[file_path] = date_time
                
    return return_dict


def get_recent_files(dictionnary: dict, num: int = 10):
    # Triez le dictionnaire en fonction des dates de modification (values) de manière décroissante
    sorted_files = sorted(dictionnary.items(), key = operator.itemgetter(1), reverse = True)
    
    filtered_files = [(path, date) for path, date in sorted_files if "bak" not in path and os.path.basename(os.path.dirname(path)) != 'backup']
    
    # Sélectionnez les 10 fichiers les plus récemment modifiés (ou moins si moins de 10 fichiers sont disponibles)
    all_recent_files = filtered_files[:num]
    
    # Récupérez uniquement les noms de fichiers
    recent_files = [fichier for fichier, _ in all_recent_files]
    
    return recent_files


def get_recent_files_old(directory: str, num: int = 10):
    
    files = _get_files_by_extension(directory)
    recent_files = get_recent_files(files, num = num)
    return recent_files


def get_publish_files(directory: str):
    '''
    '''
    
    filepaths = []
    
    for root, _, files in os.walk(directory):
        if os.path.basename(root) == 'publish':
            for file in files:
                if '_P.' in file:
                    filepaths.append(os.path.join(root, file))
    
    return filepaths
