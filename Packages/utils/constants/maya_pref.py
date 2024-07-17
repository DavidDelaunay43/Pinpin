import os
from Packages.utils.constants.pinpin import PACKAGES_PATH
from Packages.utils.funcs import is_four_digits, find_directory

MAYA_INTEG_PATH = os.path.join(PACKAGES_PATH, 'apps', 'maya_app', 'integration')

ICONS = [
    'alembic_icon.png',
    'create_asset_icon.png',
    'gpu_cache_icon.png',
    'pinpin_icon.png',
    'publish_icon.png',
    'save_as_icon.png',
    'set_project_icon.png',
    'thumbnail_icon.png',
    'usd_icon.ico'
]

MENU_PINPIN_NAME = 'menu_pinpinMenu.mel'
SHELF_PINPIN_NAME = 'shelf_Pinpin.mel'
USER_SETUP_NAME = 'userSetup.py'

ICONS_PATHS_SOURCE = [os.path.join(MAYA_INTEG_PATH, icon) for icon in ICONS]

MENU_PINPIN_SOURCE = os.path.join(MAYA_INTEG_PATH, MENU_PINPIN_NAME)
SHELF_PINPIN_SOURCE = os.path.join(MAYA_INTEG_PATH, SHELF_PINPIN_NAME)
USER_SETUP_SOURCE = os.path.join(MAYA_INTEG_PATH, USER_SETUP_NAME)

#
documents_path = os.path.join(os.path.expanduser("~"), 'Documents')
MAYA_PREF_PATH = os.path.join(documents_path, find_directory(documents_path, 'maya'))
MAYA_YEAR_PATH = next((os.path.join(MAYA_PREF_PATH, dir) for dir in os.listdir(MAYA_PREF_PATH) if is_four_digits(dir)), None)

MAYA_SHELF_PATH = os.path.join(MAYA_YEAR_PATH, 'prefs', 'shelves')
MAYA_MENU_PATH = os.path.join(MAYA_YEAR_PATH, 'prefs', 'markingMenus')
MAYA_SCRIPTS_PATH = os.path.join(MAYA_YEAR_PATH, 'scripts')
MAYA_ICON_PATH = os.path.join(MAYA_YEAR_PATH, 'prefs', 'icons')

