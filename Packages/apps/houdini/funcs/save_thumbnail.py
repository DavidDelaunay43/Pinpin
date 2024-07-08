import hou
import os
from Packages.utils.constants.constants_old import CURRENT_PROJECT_PREVIEW_FOLDER

def save_thumbnail():
    cur_desktop = hou.ui.curDesktop()
    desktop = cur_desktop.name()
    viewer = hou.paneTabType.SceneViewer
    panetab = cur_desktop.paneTabOfType(viewer).name()
    persp = cur_desktop.paneTabOfType(viewer).curViewport().name()
    camera_path = desktop + '.' + panetab + '.' + 'world.' + persp

    file_name = os.path.basename(hou.hipFile.path())
    output_path = os.path.join(CURRENT_PROJECT_PREVIEW_FOLDER, f"{file_name}.png")
    
    if os.path.exists(output_path):
        os.remove(output_path)

    hou.hscript(f"viewwrite -r 180 101 -f 0 0 {camera_path} '{output_path}'")
