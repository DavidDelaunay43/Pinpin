import os
import shutil
from maya import cmds
import maya.api.OpenMaya as om
from Packages.apps.maya_app.funcs.playblast import create_thumbnail, update_thumbnail
from Packages.logic.filefunc import return_increment_edit
from Packages.logic.filefunc.publish_funcs import find_publish_directory
from Packages.logic.filefunc.get_funcs import return_publish_name, get_files, return_increment_publish_name
from Packages.logic.json_funcs import set_recent_file
from Packages.apps.maya_app.funcs.debug_funcs import delete_colon, list_shading_nodes

def increment_edit():
    '''
    '''

    current_file_path = cmds.file(query = True, sceneName = True)
    current_file_name = os.path.basename(current_file_path)
    parent_directory = os.path.dirname(current_file_path)

    new_file_name = return_increment_edit(current_file_path)
    new_file_path = os.path.join(parent_directory, new_file_name)

    cmds.file(rename = new_file_path)
    cmds.file(save = True)
    om.MGlobal.displayInfo(f'{new_file_name} saved.')
    set_recent_file(new_file_path)

    update_thumbnail()

def publish(del_colon: bool = True, variant: str = ''):
    '''
    étapes :
    0 - indentifier le path et le name du fichier courant
    1 - identifier le répertoire de publish
    2 - créer le publish name et le publish directory
    3 - s'il y a déjà un publish
        incrémenter et déplacer le publish existant dans le répertoire old
    4 - exporter la sélection 
    '''

    # 0
    current_file_path = cmds.file(query = True, sceneName = True)
    current_file_name = os.path.basename(current_file_path)

    # 1 
    publish_directory = find_publish_directory(current_file_path)
    
    # 2 
    publish_file_name = return_publish_name(current_file_name) # CDS_chr_petru_ldv_P.ma
    
    # variant
    if variant != '':
        pfx, asset_type, asset_name, department, end = publish_file_name.split('_')
        asset_name = f'{asset_name}{variant}'
        publish_file_name = '_'.join([pfx, asset_type, asset_name, department, end])
    
    publish_file_directory = os.path.join(publish_directory, publish_file_name)
    # 3
    if not os.path.exists(publish_file_directory):
        cmds.file(publish_file_directory, force = True, options = "v=0", type = "mayaAscii", exportSelected = True, preserveReferences = False)
        create_thumbnail(publish_file_name, increment = True)
        return
    
    old_publish_directory = os.path.join(publish_directory, 'old') # path du répertoire old
    os.mkdir(old_publish_directory) if not os.path.exists(old_publish_directory) else None # créer le répertoire old s'il n'existe pas
    old_publish_list = get_files(old_publish_directory, exclude_type = [".txt", '.mel', '.db', '.usd'])

    # garder que les publish de l'objet
    old_publish_list_filtered = []
    for old_file in old_publish_list:
        old_file_base_name = os.path.splitext(publish_file_name)[0]
        if old_file.startswith(old_file_base_name):
            old_publish_list_filtered.append(old_file)

    old_publish_list = old_publish_list_filtered
    old_publish_list.sort()

    new_increment_publish_name = return_increment_publish_name(publish_file_name, old_publish_list) # trouver le dernier incrément
    os.rename(publish_file_directory, os.path.join(publish_directory, new_increment_publish_name)) # renommer le dernier publish par le denrier incrément
    shutil.move(os.path.join(publish_directory, new_increment_publish_name), old_publish_directory) # déplacer le dernier pulbish dans old

    # 4
    cmds.file(publish_file_directory, force = True, options = "v=0", type = "mayaAscii", exportSelected = True, preserveReferences = False)
    create_thumbnail(publish_file_name, increment = True)
    
    # 5 delete colon
    if del_colon:
        shading_nodes = list_shading_nodes()
        delete_colon(publish_file_directory, shading_nodes)
