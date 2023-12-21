import json

def json_to_dict(json_file_path: str) -> dict:
    '''
    Convertit un fichier JSON en un dictionnaire Python.

    Args:
        json_file_path (str): Le chemin du fichier JSON à convertir en dictionnaire.

    Returns:
        dict: Le dictionnaire Python résultant à partir du fichier JSON.
    '''
    
    with open(json_file_path, 'r', encoding = 'utf-8') as file:
        dico = json.load(file)
        
    return dico

def dict_to_json(dictionary: dict, json_file_path: str) -> None:
    '''
    Convertit un dictionnaire Python en un fichier JSON.

    Args:
        dictionary (dict): Le dictionnaire Python à convertir en JSON.
        json_file_path (str): Le chemin du fichier JSON de destination.
    '''
    
    with open(json_file_path, 'w', encoding = 'utf-8') as file:
        json.dump(dictionary, file, indent = 4, ensure_ascii = False)
