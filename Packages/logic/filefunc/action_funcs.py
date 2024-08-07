import os
import shutil
from Packages.logic.filefunc import get_funcs

def increment_file_external(file_path: str) -> str:
    '''Copie un fichier spécifié vers le même répertoire en incrémentant le suffixe numérique
    au nom du fichier pour le différencier de la version précédente.

    Args :
    file_path (str) : Le chemin absolu du fichier à copier.

    Return :
    str : Le chemin absolu du nouveau fichier créé avec un nom incrémenté.

    '''
    
    parent_directory: str = os.path.dirname(file_path)
    new_file_name: str = get_funcs.return_increment_edit(file_path)
    new_file_path: str = os.path.join(parent_directory, new_file_name)
    shutil.copy(file_path, new_file_path)
    return new_file_path
