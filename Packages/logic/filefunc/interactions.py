from subprocess import Popen


def open_explorer(path: str):
    '''Ouvre l'explorateur de fichiers de Windows pour afficher le contenu du répertoire spécifié.

    Args :
    path (str) : Le chemin du répertoire à ouvrir dans l'explorateur de fichiers.
    '''
    
    path = path.replace('/', '\\')
    Popen(['explorer', path])