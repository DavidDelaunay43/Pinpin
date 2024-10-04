import os
import shutil
import sys
from PySide2.QtWidgets import QApplication, QDialog
from Packages.apps.standalone_old.main_window_standalone import MainWindowStandalone
from Packages.logic.json_funcs.convert_funcs import dict_to_json
from Packages.utils.constants.version import VERSION, USER_VERSION
from Packages.utils.constants.project_pinpin_data import CURRENT_PROJECT
from Packages.utils.constants.preferences import (
    USER_PREFS, BLANK_PREFS,
    VERSION_JSON_PATH, BLANK_VERSION_JSON_PATH,
    APPS_JSON_PATH
)
from Packages.utils.constants.maya_pref import (
    ICONS, ICONS_PATHS_SOURCE,
    MENU_PINPIN_NAME, MENU_PINPIN_SOURCE,
    SHELF_PINPIN_NAME, SHELF_PINPIN_SOURCE,
    USER_SETUP_NAME, USER_SETUP_SOURCE,
    MAYA_SHELF_PATH, MAYA_MENU_PATH, MAYA_SCRIPTS_PATH, MAYA_ICON_PATH
)
from Packages.utils.constants.houdini_pref import (
    H_MENU_PINPIN_NAME, H_MENU_PINPIN_SOURCE,
    H_SHELF_PINPIN_NAME, H_SHELF_PINPIN_SOURCE,
    HOUDINI_SHELF_PATH, HOUDINI_MENU_PATH
)
from Packages.utils.app_finder import AppFinder
from Packages.utils.init_project import InitProject

#logger = init_logger(__file__)


class PinpinApp(QApplication):
    
    
    VERSION = VERSION
    USER_VERSION = USER_VERSION
    
    
    def __init__(self, argv = sys.argv):
        super(PinpinApp, self).__init__(argv)
        self.check_pref()
        self.find_apps()
        
        if CURRENT_PROJECT == '':
            init_project_dialog = InitProject()
            init_project_dialog.exec_()
            
            if not init_project_dialog.ACCEPTED:
                self.quit()
                sys.exit(0)
                
        self.create_main_window()
        
        
    def find_apps(self):
        apps_dict = AppFinder().app_dict
        #dict_to_json(dictionary=apps_dict, json_file_path=APPS_JSON_PATH)
        import json
        
        with open(APPS_JSON_PATH, 'w', encoding = 'utf-8') as file:
            json.dump(apps_dict, file, indent = 4, ensure_ascii = False)
    

    def check_pref(self):
        self.check_pinpin_pref()
        self.check_maya_pref()
        self.check_houdini_pref()
        
    
    def check_pinpin_pref(self):
        if not os.path.exists(USER_PREFS):
            shutil.copytree(BLANK_PREFS, USER_PREFS)
            return
        
        for json_file in os.listdir(BLANK_PREFS):
            
            json_file_path: str = os.path.join(USER_PREFS, json_file)
            if not os.path.exists(json_file_path):
                shutil.copy(os.path.join(BLANK_PREFS, json_file), USER_PREFS)
                
                
    def check_maya_pref(self):
        if not os.path.exists(os.path.join(MAYA_SHELF_PATH, SHELF_PINPIN_NAME)):
            shutil.copy(SHELF_PINPIN_SOURCE, MAYA_SHELF_PATH)
        
        if not os.path.join(os.path.join(MAYA_MENU_PATH, MENU_PINPIN_NAME)):
            shutil.copy(MENU_PINPIN_SOURCE, MAYA_MENU_PATH)
        
        if not os.path.exists(os.path.join(MAYA_SCRIPTS_PATH, USER_SETUP_NAME)):
            shutil.copy(USER_SETUP_SOURCE, MAYA_SCRIPTS_PATH)
        
        for icon, icon_source in zip(ICONS, ICONS_PATHS_SOURCE):
            if not os.path.exists(os.path.join(MAYA_ICON_PATH, icon)):
                shutil.copy(icon_source, MAYA_ICON_PATH)
                
                
    def check_houdini_pref(self):
        if not os.path.exists(os.path.join(HOUDINI_SHELF_PATH, H_SHELF_PINPIN_NAME)):
            shutil.copy(H_SHELF_PINPIN_SOURCE, HOUDINI_SHELF_PATH)
            
        if not os.path.exists(os.path.join(HOUDINI_MENU_PATH, H_MENU_PINPIN_NAME)):
            shutil.copy(H_MENU_PINPIN_SOURCE, HOUDINI_MENU_PATH)
               
                        
    def update_pinpin_pref(self):
        if self.VERSION == self.USER_VERSION:
            return
        
        os.remove(VERSION_JSON_PATH)
        shutil.copy(BLANK_VERSION_JSON_PATH, USER_PREFS)
        
        self.update_maya_prefs()
        self.update_houdini_prefs()
           
    
    def update_maya_prefs(self):
        maya_shelf_path: str = os.path.join(MAYA_SHELF_PATH, SHELF_PINPIN_NAME)
        if os.path.exists(maya_shelf_path):
            os.remove(maya_shelf_path)
        shutil.copy(SHELF_PINPIN_SOURCE, MAYA_SHELF_PATH)
        
        maya_menu_path: str = os.path.join(MAYA_MENU_PATH, MENU_PINPIN_NAME)
        if os.path.join(maya_menu_path):
            os.remove(maya_menu_path)
        shutil.copy(MENU_PINPIN_SOURCE, MAYA_MENU_PATH)
        
        maya_scripts_path = os.path.join(MAYA_SCRIPTS_PATH, USER_SETUP_NAME)
        if os.path.exists(maya_scripts_path):
            os.remove(maya_scripts_path)
        shutil.copy(USER_SETUP_SOURCE, MAYA_SCRIPTS_PATH)
        
        for icon, icon_source in zip(ICONS, ICONS_PATHS_SOURCE):
            if os.path.exists(os.path.join(MAYA_ICON_PATH, icon)):
                os.remove(os.path.join(MAYA_ICON_PATH, icon))
            shutil.copy(icon_source, MAYA_ICON_PATH)
    
    
    def update_houdini_prefs(self):
        houdini_shelf_path: str = os.path.join(HOUDINI_SHELF_PATH, H_SHELF_PINPIN_NAME)
        if os.path.exists(houdini_shelf_path):
            os.remove(houdini_shelf_path)
        shutil.copy(H_SHELF_PINPIN_SOURCE, HOUDINI_SHELF_PATH)
        
        houdini_menu_path = os.path.join(HOUDINI_MENU_PATH, H_MENU_PINPIN_NAME)
        if os.path.exists(houdini_menu_path):
            os.remove(houdini_menu_path)
        if not os.path.exists(HOUDINI_MENU_PATH):
            os.mkdir(HOUDINI_MENU_PATH)
        shutil.copy(H_MENU_PINPIN_SOURCE, HOUDINI_MENU_PATH)
    
    
    def create_main_window(self):
        self.window = MainWindowStandalone()
        self.window.show()
