import os
from Packages.utils.funcs import find_package_path, get_current

# Software directories
ROOT_NAME = "Pinpin"    
ROOT_PATH = find_package_path(ROOT_NAME)
PREF_DEFAULT_PATH = os.path.join(ROOT_PATH, '.pinpin')
VERSION = get_current(os.path.join(PREF_DEFAULT_PATH, 'version.json'), 'version')
UNINSTALL_PATH = os.path.join(ROOT_PATH, "unins000.exe")
SITE_PACKAGES_PATH = os.path.join(ROOT_PATH, "bin", "lib")

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

# User
USERNAME = f'{os.getenv("USERNAME")}'

USER_DIR = os.path.expanduser("~")

PREFS = os.path.join(USER_DIR, '.pinpin')

LOGS_PATH =os.path.join(PREFS, 'logs')

CLICKED_ITEMS_JSON_PATH = os.path.join(PREFS, 'clicked_items.json')

UI_PREFS_JSON_PATH = os.path.join(PREFS, 'ui_prefs.json')

NUM_FILES = get_current(UI_PREFS_JSON_PATH, 'num_files')
REVERSE_SORT_FILES = get_current(UI_PREFS_JSON_PATH, 'reverse_sort_file')

#STYLE_JSON_PATH = os.path.join(PREFS, "style.json")

PROJECT_JSON_PATH = os.path.join(PREFS, "project_esma.json")
APPS_JSON_PATH = os.path.join(PREFS, 'apps_esma.json')
DEV_MODE_JSON = os.path.join(PREFS, 'dev_mode.json')
RECENT_FILES_JSON = os.path.join(PREFS, 'recent_files.json')
SPECIAL_UI_JSON = os.path.join(PREFS, 'special_ui.json')
# Json files
#STYLES_LIST = get_list(STYLE_JSON_PATH, 'styles')
CURRENT_STYLE = os.path.join(STYLE_PATH, 'biiiped.qss')
PALETTE_PATH = os.path.join(STYLE_PATH, 'palette_1.json')
SPECIAL_STYLE = os.path.join(r'\\GANDALF\3d4_23_24\_partage\pinpin\qs', 'biiiped.qss')

EXTS = {
    ".abc": "fbxreview",
    ".blend": "blender",
    ".fbx": "fbxreview",
    ".kra": "krita",
    ".hip": "houdini",
    ".hipnc": "houdini",
    ".ma": "maya",
    ".mb": "maya",
    ".nk": "nuke",
    ".obj": "fbxreview",
    ".psd": "photoshop",
    ".drp": "resolve",
    ".uasset": "unreal",
    ".zpr": "zbrush",
    ".ztl": "zbrush",
    ".zpr": "zbrush",
    ".spp": "substance_painter",
    ".sbs": "substance_designer",
    ".sbsar": "substance_designer",
    ".png": "it",
    ".exr": "it",
    ".tex": "it",
    ".usd": "usdview",
    ".usda": "usdview"
}

# INTEGRATION
MAYA_SHELF_PATH = os.path.join(USER_DIR, 'Documents', 'maya', '2023', 'pref', 'shelves')
MAYA_SHELF_SOURCE_PATH = os.path.join(ROOT_PATH, 'Packages', 'apps', 'integration', 'shelf_Pinpin.mel')

# Current project informations
_CURRENT_PROJECT = get_current(PROJECT_JSON_PATH, 'current_project')
CURRENT_PROJECT_NAME, CURRENT_PROJECT_PATH = next(iter(_CURRENT_PROJECT.items()))
CURRENT_PROJECT_DATA_FOLDER = os.path.join(CURRENT_PROJECT_PATH, '.pinpin_data'.lower())
CURRENT_PROJECT_PREVIEW_FOLDER = os.path.join(CURRENT_PROJECT_DATA_FOLDER, 'preview'.lower())
CURRENT_PROJECT_ICON_FOLDER = os.path.join(CURRENT_PROJECT_DATA_FOLDER, 'icons'.lower())
FILE_DATA_JSON_PATH = os.path.join(CURRENT_PROJECT_DATA_FOLDER, 'file_data.json')
PREFIX_JSON_PATH = os.path.join(CURRENT_PROJECT_DATA_FOLDER, 'prefix.json')
PREFIX = get_current(PREFIX_JSON_PATH, 'prefix')

ASSET_DIR = os.path.join(CURRENT_PROJECT_PATH, '04_asset')
SEQUENCE_DIR = os.path.join(CURRENT_PROJECT_PATH, '05_sequence')
SHOT_DIR = os.path.join(CURRENT_PROJECT_PATH, '06_shot')
COMP_DIR = os.path.join(CURRENT_PROJECT_PATH, '07_comp')
PUBLISH_DIR = os.path.join(CURRENT_PROJECT_PATH, '09_publish')
TEX_DIR = os.path.join(CURRENT_PROJECT_PATH, '10_texture')
CACHE_DIR = os.path.join(CURRENT_PROJECT_PATH, '11_cache')
