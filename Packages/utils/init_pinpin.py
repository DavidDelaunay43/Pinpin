from datetime import datetime
import logging
from pathlib import Path
import shutil
from Packages.utils.app_finder import AppFinder
from Packages.utils.core import Core
from Packages.utils.data_class import SoftwarePaths, PreferencesPaths
from Packages.utils.enums import Root
from Packages.utils.json_file import JsonFile
from Packages.utils.logger import Logger
from Packages.utils.send_email import Email


class InitPinpin:
    
    
    PINPIN_PATH: Path = Core.pinpin_path()
    
    # User
    USERNAME: str = Core.username()
    USERDIR: Path = Core.user_dir()
    DOCUMENTS_DIR: Path = Core.documents_dir()
    
    # Preferences
    PREFS_PATHS_SOURCE: PreferencesPaths = Core.prefs_paths(Root.SOURCE)
    PREFS_PATHS_DEST: PreferencesPaths = Core.prefs_paths(Root.DEST)
    
    PREFS_ROOTPATH_SOURCE: Path = PREFS_PATHS_SOURCE.USER_PREFS_ROOT
    PREFS_ROOTPATH_DEST: Path = PREFS_PATHS_DEST.USER_PREFS_ROOT
    
    VERSION_FILE_SOURCE: JsonFile = PREFS_PATHS_SOURCE.VERSION_JSONFILE
    VERSION_FILE_DEST: JsonFile = PREFS_PATHS_DEST.VERSION_JSONFILE
    
    APPS_FILE_DEST: JsonFile = PREFS_PATHS_DEST.APPS_JSONFILE
    
    # Softwares
    MAYA_INFOS: SoftwarePaths = Core.maya_infos()
    HOUDINI_INFOS: SoftwarePaths = Core.houdini_infos()
    
    SOURCE_PATHS: tuple[Path] = (
        MAYA_INFOS.PINPIN_MENU_SOURCE_PATH,
        MAYA_INFOS.PINPIN_SHELF_SOURCE_PATH,
        HOUDINI_INFOS.PINPIN_MENU_SOURCE_PATH,
        HOUDINI_INFOS.PINPIN_SHELF_SOURCE_PATH
    )
    
    DEST_PATHS: tuple[Path] = (
        MAYA_INFOS.PINPIN_MENU_DEST_PATH,
        MAYA_INFOS.PINPIN_SHELF_DEST_PATH,
        HOUDINI_INFOS.PINPIN_MENU_DEST_PATH,
        HOUDINI_INFOS.PINPIN_SHELF_DEST_PATH
    )
    
    
    @classmethod
    def new_version(cls) -> bool:
        
        if not cls.VERSION_FILE_DEST.exists():
            cls.copy_file(cls.VERSION_FILE_SOURCE.path, cls.VERSION_FILE_DEST.path)
            return True
        
        return cls.VERSION_FILE_DEST.get_value('version') == cls.VERSION_FILE_SOURCE.get_value('version')
    
    
    @classmethod
    def check_preferences(cls, override: bool = False) -> None:
        
        if not cls.PREFS_ROOTPATH_DEST.exists() or override:
            cls.copy_pinpin_preferences()
    
    
    @classmethod
    def copy_pinpin_preferences(cls) -> None:
        
        if cls.PREFS_ROOTPATH_DEST.exists():
            shutil.rmtree(cls.PREFS_ROOTPATH_DEST)
        
        shutil.copytree(cls.PREFS_ROOTPATH_SOURCE, cls.PREFS_ROOTPATH_DEST)
        Logger.info(f'Copy Pinpin preferences -> {cls.PREFS_ROOTPATH_DEST}')
    
    
    @classmethod
    def check_apps_data(cls) -> None:
        
        if not AppFinder.json_is_empty(cls.APPS_FILE_DEST.path):
            return
        
        AppFinder.find_3d_applications()
        AppFinder.write_json_file(cls.APPS_FILE_DEST.path)
        Logger.info(f'Find 3d applications and write -> {cls.APPS_FILE_DEST.path}')
        
        
    @classmethod
    def check_current_project(cls) -> None:
        
        current_project: Path = cls.PREFS_PATHS_DEST.CURRENT_PROJECT_JSONFILE.get_value('current_project')
        
        if current_project:
            Logger.info(f'Current project is: {current_project}')
            return
        
        cls.PREFS_PATHS_DEST.CURRENT_PROJECT_JSONFILE.set_value('current_project', cls.PREFS_PATHS_DEST.FAKE_PROJECT_DIRPATH)
        Logger.info(f'Set current project: {cls.PREFS_PATHS_DEST.FAKE_PROJECT_DIRPATH}')
        
    
    # Software
    @classmethod
    def check_soft_integrations(cls, override: bool = False) -> None:
        
        Logger.info(f'Check 3D softwares integrations')
        
        for source_filepath, dest_filepath in zip(cls.SOURCE_PATHS, cls.DEST_PATHS):
            
            if not dest_filepath.exists() or override:
                cls.copy_file(source_filepath, dest_filepath)
            
    
    # Useful methods
    @staticmethod
    def copy_file(source_path: Path, dest_path: Path) -> None:
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, dest_path)
        Logger.info(f'Copy File:\nSource: {source_path}\nDest: {dest_path}')
    
        
def main() -> None:
    
    Logger.LOGGER_NAME = __file__
        
    InitPinpin.check_preferences()
    Logger.write_to_file(path=Core.today_log_filepath(), level=logging.DEBUG)
    
    if not InitPinpin.new_version():
        InitPinpin.check_soft_integrations()
    
    Logger.info(f'Pinpin new version: {InitPinpin.VERSION_FILE_DEST.get_value("version")}')
    InitPinpin.copy_file(InitPinpin.VERSION_FILE_SOURCE.path, InitPinpin.VERSION_FILE_DEST.path)
    InitPinpin.check_apps_data()
    InitPinpin.check_soft_integrations(override=True)
    InitPinpin.check_current_project()
    
    Email.message = f'New Pinpin installation - version {InitPinpin.VERSION_FILE_DEST.get_value("version")}'
    Email.attachment_files.append(Core.today_log_filepath())
    Email.send()
