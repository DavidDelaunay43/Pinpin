import os
import shutil
from maya import mel, cmds
import maya.api.OpenMaya as om
from Packages.apps.maya_app_old.funcs import playblast
from Packages.logic.filefunc import publish_funcs
from Packages.logic.filefunc import get_funcs
from Packages.utils.old.funcs import forward_slash

def export_usd(output_file_path: str):
    '''
    '''
    
    if not cmds.ls(selection = True):
        om.MGlobal.displayError('Nothing is selected.')
        return
    
    output_file_path = forward_slash(output_file_path)
    string = f'file -force -options ";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=0;eulerFilter=0;staticSingleSample=0;startTime=1;endTime=1;frameStride=1;frameSample=0.0;defaultUSDFormat=usdc;parentScope=;shadingMode=useRegistry;convertMaterialsTo=[];exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=1;materialsScopeName=mtl" -typ "USD Export" -pr -es "{output_file_path}";'
    mel.eval(string)
    om.MGlobal.displayInfo(f'USD exported : {output_file_path}')

def publish_usd_asset():
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
    publish_directory = publish_funcs.find_publish_directory(current_file_path)
    
    # 2 
    publish_file_name = get_funcs.return_publish_name(current_file_name)
    publish_file_name = publish_file_name.replace('.ma', '.usd')
    publish_file_directory = os.path.join(publish_directory, publish_file_name)

    # 3
    if not os.path.exists(publish_file_directory):
        export_usd(publish_file_directory)
        playblast.create_thumbnail(publish_file_name, increment = True, ext = '.usd')
        return

    old_publish_directory = os.path.join(publish_directory, 'old') # path du répertoire old
    os.mkdir(old_publish_directory) if not os.path.exists(old_publish_directory) else None # créer le répertoire old s'il n'existe pas
    old_publish_list = get_funcs.get_files(old_publish_directory, exclude_type = [".txt", '.mel', '.db', '.ma', '.mb'])
    for old_file in old_publish_list:
        if not old_file.startswith(os.path.splitext(publish_file_name)[0]):
            old_publish_list.remove(old_file)

    new_increment_publish_name = get_funcs.return_increment_publish_name(publish_file_name, old_publish_list) # trouver le dernier incrément
    os.rename(publish_file_directory, os.path.join(publish_directory, new_increment_publish_name)) # renommer le dernier publish par le denrier incrément
    shutil.move(os.path.join(publish_directory, new_increment_publish_name), old_publish_directory) # déplacer le dernier pulbish dans old

    # 4
    export_usd(publish_file_directory)
    playblast.create_thumbnail(publish_file_name, increment = True, ext = '.usd')
