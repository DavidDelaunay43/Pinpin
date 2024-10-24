import os
from Packages.utils.old.funcs import find_package_path, get_current_value

# Software directories
ROOT_NAME = "Pinpin"    
ROOT_PATH = find_package_path(ROOT_NAME)
PREF_DEFAULT_PATH = os.path.join(ROOT_PATH, '.pinpin')
VERSION = get_current_value(os.path.join(PREF_DEFAULT_PATH, 'version.json'), 'version')
UNINSTALL_PATH = os.path.join(ROOT_PATH, "unins000.exe")
SITE_PACKAGES_PATH = os.path.join(ROOT_PATH, "bin", "lib")

PYTHON_W = os.path.join(ROOT_PATH, '.venv', 'Scripts', 'pythonw.exe')

# Project Files
PROJECT_FILES_PATH = os.path.join(ROOT_PATH, "ProjectFiles")

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

PINPIN_APP_ICON_PATH = os.path.join(ROOT_PATH, 'pinpin_app_icon.py')
QRC_PATH = os.path.join(ROOT_PATH, 'ressources.qrc')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from Packages.utils.constants.project_pinpin_data import CURRENT_PROJECT

ASSET_DIR = os.path.join(CURRENT_PROJECT, '04_asset')
SEQUENCE_DIR = os.path.join(CURRENT_PROJECT, '05_sequence')
SHOT_DIR = os.path.join(CURRENT_PROJECT, '06_shot')
COMP_DIR = os.path.join(CURRENT_PROJECT, '07_comp')
PUBLISH_DIR = os.path.join(CURRENT_PROJECT, '09_publish')
TEX_DIR = os.path.join(CURRENT_PROJECT, '10_texture')
CACHE_DIR = os.path.join(CURRENT_PROJECT, '11_cache')
