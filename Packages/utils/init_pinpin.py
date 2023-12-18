import os
import json
import shutil
import datetime
from Packages.utils.funcs import find_package_path, get_current

ROOT_NAME = "Pinpin"    
ROOT_PATH = find_package_path(ROOT_NAME)
PREF_SOURCE_PATH = os.path.join(ROOT_PATH, '.pinpin')
USER_DIR = os.path.expanduser("~")
PREFS = os.path.join(USER_DIR, '.pinpin')

def get_file_modification_date_time(file_path: str):
    '''
    '''
    
    file_stat = os.stat(file_path)
    modification_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)
    return modification_time

def check_new_version():
    '''
    '''

    VERSION_JSON_FILE_PATH = os.path.join(PREF_SOURCE_PATH, 'version.json')
    version = get_current(VERSION_JSON_FILE_PATH, 'version')
    return version

def check_existing_version():
    '''
    '''

    VERSION_JSON_FILE_PATH = os.path.join(PREFS, 'version.json')
    version = get_current(VERSION_JSON_FILE_PATH, 'version')
    return version

def update_houdini_prefs():
    '''
    '''
    
    print('UPDATE HOUDINI PREFS')
    
    HOUDINI_SOURCE_PATH = os.path.join(ROOT_PATH, 'Packages', 'apps', 'houdini', 'integration')
    HOUDINI_PREFS = os.path.join(USER_DIR, 'Documents', 'houdini19.5')

    if not os.path.exists(HOUDINI_PREFS):
        return
    
    shelf_file = 'pinpin.shelf'
    shelf_file_source = os.path.join(HOUDINI_SOURCE_PATH, shelf_file)
    shelf_file_dest = os.path.join(HOUDINI_PREFS, 'toolbar')
    
    if not os.path.exists(shelf_file_dest):
        os.mkdir(shelf_file_dest)
        
    if os.path.exists(os.path.join(shelf_file_dest, shelf_file)):
        os.remove(os.path.join(shelf_file_dest, shelf_file))
    shutil.copy(shelf_file_source, shelf_file_dest)
        
    # ---------------------------------------------------------------------------------------------------------
    
    radial_menu_file = 'pinpin.radialmenu'
    radial_menu_file_source = os.path.join(HOUDINI_SOURCE_PATH, radial_menu_file)
    radial_menu_file_dest = os.path.join(HOUDINI_PREFS, 'radialmenu')
    
    if not os.path.exists(radial_menu_file_dest):
        os.mkdir(radial_menu_file_dest)

    if os.path.exists(os.path.join(radial_menu_file_dest, radial_menu_file)):
        os.remove(os.path.join(radial_menu_file_dest, radial_menu_file))
    shutil.copy(radial_menu_file_source, radial_menu_file_dest)

def update_maya_prefs():
    '''
    '''

    print('UPDATE MAYA PREFS')

    SHELF_FILE = 'shelf_Pinpin.mel'
    MARKING_MENU_FILE = 'menu_pinpinMenu.mel'
    USER_SETUP_FILE = 'userSetup.py'

    MAYA_SHELF_PATH = os.path.join(USER_DIR, 'Documents', 'maya', '2023', 'prefs', 'shelves')
    MAYA_MENU_PATH = os.path.join(USER_DIR, 'Documents', 'maya', '2023', 'prefs', 'markingMenus')
    MAYA_SCRIPTS_PATH = os.path.join(USER_DIR, 'Documents', 'maya', 'scripts')

    MAYA_SOURCE_PATH = os.path.join(ROOT_PATH, 'Packages', 'apps', 'maya_app', 'integration')
    MAYA_SHELF_SOURCE_PATH = os.path.join(MAYA_SOURCE_PATH, SHELF_FILE)
    MAYA_MENU_SOURCE_PATH = os.path.join(MAYA_SOURCE_PATH, MARKING_MENU_FILE)
    MAYA_USERSETUP_SOURCE_PATH = os.path.join(MAYA_SOURCE_PATH, USER_SETUP_FILE)

    # userSetup.py
    if os.path.exists(os.path.join(MAYA_SCRIPTS_PATH, 'userSetup.py')):
        os.remove(os.path.join(MAYA_SCRIPTS_PATH, 'userSetup.py'))
    shutil.copy(MAYA_USERSETUP_SOURCE_PATH, MAYA_SCRIPTS_PATH)

    # shelf
    if os.path.exists(os.path.join(MAYA_SHELF_PATH, 'shelf_Pinpin.mel')):
        os.remove(os.path.join(MAYA_SHELF_PATH, 'shelf_Pinpin.mel'))
    shutil.copy(MAYA_SHELF_SOURCE_PATH, MAYA_SHELF_PATH)

    # marking menu
    if os.path.exists(os.path.join(MAYA_MENU_PATH, 'menu_pinpinMenu.mel')):
        os.remove(os.path.join(MAYA_MENU_PATH, 'menu_pinpinMenu.mel'))
    shutil.copy(MAYA_MENU_SOURCE_PATH, MAYA_MENU_PATH)

    #
    MAYA_ICON_DEST_PATH = os.path.join(USER_DIR, 'Documents', 'maya', '2023', 'prefs', 'icons')
    files = (
        'pinpin_icon.png',
        'publish_icon.png',
        'save_as_icon.png',
        'thumbnail_icon.png',
        'usd_icon.ico'
    )

    for file in files:

        source_file_path = os.path.join(MAYA_SOURCE_PATH, file)
        dest_file_path = os.path.join(MAYA_ICON_DEST_PATH, file)

        if os.path.exists(dest_file_path):
            os.remove(dest_file_path)
        shutil.copy(source_file_path, MAYA_ICON_DEST_PATH)

def update_pinpin_prefs():
    '''
    '''

    CLICKED_ITEMS_SOURCE_PATH = os.path.join(PREF_SOURCE_PATH, 'clicked_items.json')
    VERSION_SOURCE_PATH = os.path.join(PREF_SOURCE_PATH, 'version.json')
    APPS_SOURCE_PATH = os.path.join(PREF_SOURCE_PATH, 'apps_esma.json')

    CLICKED_ITEMS_PREF_PATH = os.path.join(PREFS, 'clicked_items.json')
    VERSION_PREF_PATH = os.path.join(PREFS, 'version.json')
    APPS_PREF_PATH = os.path.join(PREFS, 'apps_esma.json')

    if not os.path.exists(PREFS):
        shutil.copytree(PREF_SOURCE_PATH, PREFS)

    else:
        if os.path.exists(CLICKED_ITEMS_PREF_PATH):
            os.remove(CLICKED_ITEMS_PREF_PATH)
        shutil.copy(CLICKED_ITEMS_SOURCE_PATH, PREFS)

        if os.path.exists(VERSION_PREF_PATH):
            os.remove(VERSION_PREF_PATH)
        shutil.copy(VERSION_SOURCE_PATH, PREFS)

        if os.path.exists(APPS_PREF_PATH):
            os.remove(APPS_PREF_PATH)
        shutil.copy(APPS_SOURCE_PATH, PREFS)
        
        #
        if not os.path.exists(os.path.join(PREFS, 'recent_files.json')):
            shutil.copy(os.path.join(PREF_SOURCE_PATH, 'recent_files.json'), PREFS)
        #

    APPS_ESMA_PATH = os.path.join(PREFS, 'apps_esma.json')
    with open(APPS_ESMA_PATH, 'r') as file:
        data = json.load(file)

    data['houdini']['pref'] = os.path.join(USER_DIR, 'Documents', 'houdini19.5')
    data['maya']['pref'] = os.path.join(USER_DIR, 'Documents', 'maya')
    data['nuke']['pref'] = os.path.join(USER_DIR, '.nuke')

    with open(APPS_ESMA_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent = 4, ensure_ascii=False)

def init_pinpin():
    '''
    '''
    print("Init pinpin")

    if not os.path.exists(PREFS):
        update_pinpin_prefs()

    existing_version = check_existing_version()
    new_version = check_new_version()

    if new_version != existing_version :
        print('Nouvelle version')
        update_houdini_prefs()
        update_maya_prefs()
        update_pinpin_prefs()
