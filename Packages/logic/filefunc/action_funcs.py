import os
import shutil
from Packages.logic.filefunc import get_funcs

def increment_file_external(file_path: str):
    '''Copie un fichier spécifié vers le même répertoire en incrémentant le suffixe numérique
    au nom du fichier pour le différencier de la version précédente.

    Args :
    file_path (str) : Le chemin absolu du fichier à copier.

    Return :
    str : Le chemin absolu du nouveau fichier créé avec un nom incrémenté.

    '''
    
    parent_directory = os.path.dirname(file_path) # récupérer le répertoire parent
    new_file_name = get_funcs.return_increment_edit(file_path) # récupérer le nom du fichier incrémenté
    new_file_path = os.path.join(parent_directory, new_file_name)
    print(new_file_path)
    print(parent_directory)
    shutil.copy(file_path, new_file_path)
    return new_file_path
