import os
from maya import cmds, mel

def ensure_directory(directory: str):
    
    if os.path.exists(directory):
        return
    
    os.makedirs(directory)

def get_gpu_cache_file_name() -> str:
    
    scene_name: str = os.path.basename(cmds.file(query = True, sceneName = True))
    prefix, seq_num, sh_num, _, _, _ = scene_name.split('_')
    alembic_file_name: str = '_'.join([prefix, seq_num, sh_num, 'layout', 'P'])
    
    return alembic_file_name

def get_directory() -> str:
    
    scene_path: str = os.path.dirname(cmds.file(query = True, sceneName = True))
    anim_path: str = os.path.dirname(scene_path)
    data_path = os.path.join(anim_path, 'data').replace('\\', '/')
    data_path = data_path.replace(r'/layout/', '/anim/')
    
    return data_path

def export_gpu_cache():
    
    file_name: str = get_gpu_cache_file_name()
    directory: str = get_directory()
    ensure_directory(directory)
    print(directory)
    
    selection = cmds.ls(selection = True)
    if not selection:
        return
    
    flags: str
    if len(selection) == 1:
        flags = selection[0]
        
    else:
        flags = ' '.join([node for node in selection])
        flags = f'-saveMultipleFiles false {flags}'
    
    gpu_cache_cmd = f'gpuCache -startTime 0 -endTime 0 -optimize -optimizationThreshold 100 -dataFormat ogawa -useBaseTessellation -directory "{directory}" -fileName "{file_name}" {flags};'
    mel.eval(gpu_cache_cmd)
