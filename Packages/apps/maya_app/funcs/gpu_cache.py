from maya import mel, cmds
import maya.api.OpenMaya as om
import os

def export_gpu_cache(file_name: str, directory: str):
    '''
    '''
    
    selected_node = cmds.ls(selection = True)[0]
    string = f'gpuCache -startTime 0 -endTime 0 -optimize -optimizationThreshold 40000 -dataFormat ogawa -directory {directory} -filename {file_name} {selected_node};'
    mel.eval(string)
    om.MGlobal.displayInfo(f'GPU Cache exported : {os.path.join(directory, file_name)}')
    