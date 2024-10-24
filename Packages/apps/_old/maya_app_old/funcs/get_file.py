__author__ = "Apolline Royer"

from maya import cmds
import os
from Packages.logic.json_funcs import set_recent_file

#IMPORTING FILES

def import_file_with_file_namespace(file_path):
    """
    Importe un fichier Maya en utilisant le nom de fichier comme namespace.

    Args:
        file_path (str): Le chemin complet vers le fichier à importer.

    Returns:
        bool: True si l'importation réussit, False en cas d'erreur.
    """
    try:
        file_name = os.path.basename(file_path)
        file_name = os.path.splitext(file_name)[0]
        cmds.file(file_path, i=1, namespace=file_name)

    except Exception as e:
        print(f"Error importing file with namespace: {e}")


def import_file_with_custom_namespace(file_path, name_space):
    """
    Importe un fichier Maya en utilisant un namespace spécifié par l'utilisateur.

    Args:
        file_path (str): Le chemin complet vers le fichier à importer.
        name_space (str): Le namespace spécifié par l'utilisateur.

    Returns:
        bool: True si l'importation réussit, False en cas d'erreur.
    """

    try:
        cmds.file(file_path, i=1, namespace=name_space)

    except Exception as e:
        print(f"Error importing file with namespace: {e}")


def import_file(file_path):
    """
    Importe un fichier Maya sans utiliser de namespace.

    Args:
        file_path (str): Le chemin complet vers le fichier à importer.

    Returns:
        bool: True si l'importation réussit, False en cas d'erreur.
    """
        
    try:
        cmds.file(file_path, i=1, namespace=":", mergeNamespacesOnClash=True)

    except Exception as e:
        print(f"Error importing file without namespace: {e}")


def import_files(namespace_type, files_paths):
    """
    Importe une liste de fichiers Maya en utilisant les mêmes options pour tous les fichiers.

    Args:
        namespace_type (str): Le type de namespace à utiliser ('file_name_as_namespace', 'specified_name_as_namespace' ou 'no_namespace').
        files_paths (list): Liste des chemins complets vers les fichiers à importer.
    """
        
    if namespace_type == 'file_name_as_namespace':
        for file_to_import in files_paths:
            import_file_with_file_namespace(file_to_import)
    elif namespace_type == 'specified_name_as_namespace':
        for file_to_import in files_paths:
            import_file_with_custom_namespace(file_to_import, 'my_namespace')
    else:
        for file_to_import in files_paths:
            import_file(file_to_import)



# REFERENCING FILES
def reference_file_with_file_namespace(file_path):
    """
    Référence un fichier Maya en utilisant le nom de fichier comme namespace.

    Args:
        file_path (str): Le chemin complet vers le fichier à référencer.

    Returns:
        bool: True si la référence réussit, False en cas d'erreur.
    """
    try:
        file_name = os.path.basename(file_path)
        file_name = os.path.splitext(file_name)[0]
        cmds.file(file_path, reference=True, namespace=file_name, sharedNodes = "shadingNetworks")

    except Exception as e:
        print(f"Error referencing file with namespace: {e}")

    
def reference_file_with_user_namespace(file_path, name_space):
    """
    Référence un fichier Maya en utilisant un namespace spécifié par l'utilisateur.

    Args:
        file_path (str): Le chemin complet vers le fichier à référencer.
        name_space (str): Le namespace spécifié par l'utilisateur.

    Returns:
        bool: True si la référence réussit, False en cas d'erreur.
    """

    try:
        cmds.file(file_path, reference=True, namespace=name_space, sharedNodes = "shadingNetworks")

    except Exception as e:
        print(f"Error referencing file with namespace: {e}")


def reference_file(file_path):
    """
    Référence un fichier Maya sans utiliser de namespace.

    Args:
        file_path (str): Le chemin complet vers le fichier à référencer.

    Returns:
        bool: True si la référence réussit, False en cas d'erreur.
    """
        
    try:
        cmds.file(file_path, reference=True, namespace=":", mergeNamespaceWithRoot=True, mergeNamespacesOnClash=True, sharedNodes = "shadingNetworks")

    except Exception as e:
        print(f"Error referencing file without namespace: {e}")


def reference_files(namespace_type, files_paths):
    """
    Référence une liste de fichiers Maya en utilisant les mêmes options pour tous les fichiers.

    Args:
        namespace_type (str): Le type de namespace à utiliser ('file_name_as_namespace', 'specified_name_as_namespace' ou 'no_namespace').
        files_paths (list): Liste des chemins complets vers les fichiers à référencer.
    """
    print('all files will be executed with the same options')
    if namespace_type == 'file_name_as_namespace':
        for file_to_ref in files_paths:
            reference_file_with_file_namespace(file_to_ref)
    elif namespace_type == 'specified_name_as_namespace':
        for file_to_ref in files_paths:
            reference_file_with_user_namespace(file_to_ref, 'my_namespace')
    else:
        for file_to_ref in files_paths:
            reference_file(file_to_ref)

#OPENING ONE SINGLE FILE
def open_maya_file(file_path):
    """
    Opens a Maya file.

    Args:
        file_path (str): The path to the Maya file to be opened.
    """
    if cmds.file(file_path, q=True, exists=True):
        cmds.file(file_path, open=True, force=True)
        print("Maya file opened successfully: " + file_path)
        set_recent_file(file_path)
    else:
        print("File does not exist: " + file_path)


#EXPORT SELECTION
def export_selected_objects(preserve_reference=False):
    """
    Export selected objects in Maya using ASCII format.

    Args:
        preserve_reference (bool): Whether to preserve references or not. Default is False.
    """
    # Get a list of selected objects
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("No objects selected for export.")
        return

    # Show the export options dialog
    export_options = 0
    if preserve_reference == True:
        export_options = 1

    result = cmds.fileDialog2(fileFilter="Maya ASCII Files (*.ma);;", dialogStyle=2, fileMode=0, caption="Export Selected", okc="Export", fm=0)

    export_path = result[0]

    # Export selected objects to the specified file in ASCII format
    cmds.select(selected_objects)
    cmds.file(export_path, exportSelected=True, type="mayaAscii", force=True, pr=export_options)
    print(f"Selected objects exported to: {export_path}")
