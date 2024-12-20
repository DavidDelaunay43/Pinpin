import logging
from pathlib import Path
import shutil
from Packages.utils.app_finder import AppFinder
from Packages.utils.core import Core
from Packages.utils.data_class import SoftwarePaths, PreferencesPaths
from Packages.utils.enums import Root
from Packages.utils.file_writer import FileWriter
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

    PREFS_FILES: tuple[Path] = (
        'apps.json',
        'current_project.json',
        'FakeProject',
        'AnOtherProject',
        'memo_path.json',
        'recent_files.json',
        'ui_prefs.json',
        'version.json'
    )
    
    
    @classmethod
    def new_version(cls) -> bool:
        
        if not cls.VERSION_FILE_DEST.exists():
            cls.copy_file(cls.VERSION_FILE_SOURCE.path, cls.VERSION_FILE_DEST.path)
            return True
        
        return cls.VERSION_FILE_DEST.get_value('version') != cls.VERSION_FILE_SOURCE.get_value('version')
    
    
    @classmethod
    def check_preferences(cls, override: bool = False) -> None:
        
        if not cls.PREFS_ROOTPATH_DEST.exists() or override:
            cls.copy_pinpin_preferences()

        cls.check_prefs_files()
        cls.check_maya_script_path()


    @classmethod
    def check_prefs_files(cls) -> None:
        
        for pref_file in cls.PREFS_FILES:

            source_file: Path = Core.pinpin_path().joinpath('.pinpin', pref_file)
            dest_file: Path = Core.user_dir().joinpath('.pinpin', pref_file)

            if not dest_file.exists():
                if source_file.is_dir():
                    shutil.copytree(source_file, dest_file)
                else:
                    shutil.copy(source_file, dest_file)
    
    
    @classmethod
    def copy_pinpin_preferences(cls) -> None:
        
        if cls.PREFS_ROOTPATH_DEST.exists():
            shutil.rmtree(cls.PREFS_ROOTPATH_DEST)
        
        shutil.copytree(cls.PREFS_ROOTPATH_SOURCE, cls.PREFS_ROOTPATH_DEST)
        Logger.info(f'Copy Pinpin preferences -> {cls.PREFS_ROOTPATH_DEST}')


    @classmethod
    def copy_pinpin_pref_file(cls, file_name: str) -> None:
        source_file_path: Path = Core.pinpin_path().joinpath(
            '.pinpin',
            file_name
        )

        if not source_file_path.exists():
            Logger.error(f'File: {source_file_path} does not exists.')
            return

        dest_file_path: Path = Core.user_dir().joinpath(
            '.pinpin',
            file_name
        )
        shutil.copy(source_file_path, dest_file_path)
    
    
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

        # Update path in maya shelf
        pinpin_path: str = str(Core.project_files_path()).replace('\\', '/')
        string: str = f'    global string $ppPath = "{pinpin_path}/";'

        FileWriter(
            path=Core.maya_infos().PINPIN_SHELF_DEST_PATH,
            string=string,
            line_index=4
        )
        Logger.debug(f'Update Maya shelf Pinpin path.')
            

    @classmethod
    def check_maya_script_path(cls) -> None:
        maya_env_file_path: Path = Core.maya_infos().PREFERENCES_PATH.joinpath('Maya.env')
        if not maya_env_file_path.exists():
            maya_env_file_path.touch()

        path_string: str = str(Core.packages_path().joinpath('apps', 'maya_app', 'integration')).replace('\\', '/')

        FileWriter(
            path=maya_env_file_path,
            string=f"MAYA_SCRIPT_PATH={path_string};"
        )

    # Useful methods
    @staticmethod
    def copy_file(source_path: Path, dest_path: Path) -> None:
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, dest_path)
        Logger.info(f'Copy File:\nSource: {source_path}\nDest: {dest_path}')
    
        
def main(force_update: bool = False) -> None:

    InitPinpin.check_preferences()
    Logger.write_to_file(path=Core.today_log_filepath(), level=logging.DEBUG)

    if InitPinpin.new_version() or force_update:
        Logger.info(f'Pinpin new version: {InitPinpin.VERSION_FILE_SOURCE.get_value("version")}')
        InitPinpin.copy_pinpin_pref_file('version.json')

        InitPinpin.check_apps_data()
        InitPinpin.check_soft_integrations(override=True)
        InitPinpin.check_current_project()

        if not Path.home().parts[-1] in ('DAVID', 'David'):
            Email.message = f'New Pinpin installation - version {InitPinpin.VERSION_FILE_SOURCE.get_value("version")}'
            Email.attachment_files.append(Core.today_log_filepath())
            Email.send()

    else:
        Logger.debug(f'Pinpin current version: {InitPinpin.VERSION_FILE_DEST.get_value("version")}')
        InitPinpin.check_apps_data()
        InitPinpin.check_soft_integrations()
        InitPinpin.check_current_project()


if __name__ == '__main__':
    main()
