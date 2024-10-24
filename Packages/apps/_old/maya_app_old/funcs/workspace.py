from maya import cmds, mel

def set_project():
    
    scene_path = cmds.file(query = True, sceneName = True)
    if scene_path == '':
        cmds.error('No project found.')
        return
    maya_path = scene_path.split('scenes')[0][:-1]
    mel.eval(f'setProject "{maya_path}";')
    print(maya_path)
