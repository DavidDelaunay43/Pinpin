import os
from Packages.utils.constants.pinpin import PINPIN_PATH


PROJECT_FILES_PATH = os.path.join(PINPIN_PATH, "ProjectFiles")

EMPTY_SCENES_PATH = os.path.join(PROJECT_FILES_PATH, "Empty_Scenes")
EMPTY_MAYA_MA_PATH = os.path.join(EMPTY_SCENES_PATH, "empty_scene_maya_2023.ma")
EMPTY_MAYA_MB_PATH = os.path.join(EMPTY_SCENES_PATH, "empty_scene_maya_2023.mb")
EMPTY_HOUDINI_PATH = os.path.join(EMPTY_SCENES_PATH, "empty_scene_houdini_19.5.hip")
EMPTY_HOUDINI_NC_PATH = os.path.join(EMPTY_SCENES_PATH, "empty_scene_houdini_19.5.hipnc")
EMPTY_NUKE_PATH = os.path.join(EMPTY_SCENES_PATH, "empty_scene_nuke_13.2v4.nk")
EMPTY_NUKE_NC_PATH = os.path.join(EMPTY_SCENES_PATH, "empty_scene_nuke_13.2v4.nknc")

FALLBACKS_PATH = os.path.join(PROJECT_FILES_PATH, 'Fallbacks')
NO_PREVIEW_FILEPATH = os.path.join(FALLBACKS_PATH, "nopreview.png")

ICON_PATH = os.path.join(PROJECT_FILES_PATH, "Icons")
PINPIN_ICON_PATH = os.path.join(ICON_PATH, 'pinpin_icon.ico')

INFOS_PATH = os.path.join(PROJECT_FILES_PATH, 'Infos')

STYLE_PATH = os.path.join(PROJECT_FILES_PATH, "Styles")
DARK_STYLE = os.path.join(STYLE_PATH, 'dark.css')

WORKSPACE_MEL_PATH = os.path.join(PROJECT_FILES_PATH, "Workspaces", "workspace.mel")

PINPIN_APP_ICON_PATH = os.path.join(PINPIN_PATH, 'pinpin_app_icon.py')
QRC_PATH = os.path.join(PINPIN_PATH, 'ressources.qrc')

CURRENT_STYLE = os.path.join(STYLE_PATH, 'biiiped.qss')
PALETTE_PATH = os.path.join(STYLE_PATH, 'palette_1.json')
