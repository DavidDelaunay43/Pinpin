import os
from maya import cmds

def ensure_directory(directory: str):
    
    if os.path.exists(directory):
        return
    
    os.makedirs(directory)

def only_mseh_in_set(set_name: str):
    
    set_members = cmds.sets(set_name, query = True, nodesOnly = True) or []

    for member in set_members:
        shapes = cmds.listRelatives(member, shapes = True) or []
        if not any(cmds.objectType(shape) == "mesh" for shape in shapes):
            return False

    return True

def get_char_sets() -> list:
    
    object_sets = cmds.ls(type = 'objectSet')
    char_sets = []
    for object_set in object_sets:
        if 'SG' in object_set:
            continue
        if only_mseh_in_set(object_set):
            if ':' in  object_set:
                char_sets.append(object_set)
                
            else:
                if '_' in  object_set:
                    char_sets.append(object_set)
                
    return char_sets

def get_time_slider_range() -> tuple:
    start_frame: float = cmds.playbackOptions(query = True, minTime = True)
    end_frame: float = cmds.playbackOptions(query = True, maxTime = True)

    return start_frame, end_frame

def get_abc_file_name(set_name: str) -> str:
    
    if ':' in set_name:
        char_name = set_name.split(':')[0]
        
    else:   
        if '_' in set_name:
            char_name = set_name.split('_')[0]
    
    scene_name: str = os.path.basename(cmds.file(query = True, sceneName = True))
    prefix, seq_num, sh_num, _, _, _ = scene_name.split('_')
    alembic_file_name: str = '_'.join([prefix, seq_num, sh_num, char_name, 'anim']) + '.abc'
    
    return alembic_file_name

def export_abc(start: int, end: int, char_set: str, directory: str):
    
    ensure_directory(directory)
    
    set_members: list = cmds.sets(char_set, query = True, nodesOnly = True)
    roots: str = ''
    for geo in set_members:
        roots += f'-root {geo} '
        
    abc_file_name: str = get_abc_file_name(char_set)
    abc_file_path: str = os.path.join(directory, abc_file_name)
    
    job_arg: str = f'-frameRange {start} {end} -uvWrite -worldSpace -writeVisibility -writeUVSets -dataFormat ogawa {roots} -file {abc_file_path}'
    cmds.AbcExport(jobArg = job_arg)

def export_alembics(start: int, end: int, char_sets: str, directory: str):
    
    for char_set in char_sets:
        export_abc(start, end, char_set, directory)

def import_abc(char_set: str, directory: str):
    
    abc_file_path: str = os.path.join(directory, get_abc_file_name(char_set))
    
    set_members: list = cmds.sets(char_set, query = True, nodesOnly = True)
    roots: str = ''
    for geo in set_members:
        roots += f'{geo} '
    
    cmds.AbcImport(abc_file_path, mode = 'import', connect = roots)
    
def import_alembics(char_sets: str, directory: str):
    
    for char_set in char_sets:
        import_abc(char_set, directory)

