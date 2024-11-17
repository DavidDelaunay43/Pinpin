from maya import cmds, mel
from Packages.utils.logger import Logger


def set_project():
    
    scene_path = cmds.file(query = True, sceneName = True)
    if scene_path == '':
        cmds.error('No project found.')
        return
    
    if not 'scenes' in scene_path:
        cmds.error('No maya workspace found.')
        return

    maya_path = scene_path.split('scenes')[0][:-1]
    mel.eval(f'setProject "{maya_path}";')
    Logger.debug(f'Set project: {maya_path}')
