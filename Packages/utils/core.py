from datetime import datetime
import os
from pathlib import Path
import re
import sys
from Packages.utils.data_class import SoftwarePaths, PreferencesInfos, PreferencesPaths, ProjectDataPaths, ProjectData
from Packages.utils.enums import Root


class Core:
    
    
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
        ".nknc": "nuke",
        ".obj": "fbxreview",
        ".psd": "photoshop",
        ".drp": "resolve",
        ".uasset": "unreal",
        ".zpr": "zbrush",
        ".ztl": "zbrush",
        ".spp": "substance_painter",
        ".sbs": "substance_designer",
        ".sbsar": "substance_designer",
        ".png": "it",
        ".exr": "it",
        ".tex": "it",
        ".usd": "usdview",
        ".usda": "usdview"
    }
    ROOT_NAME: str = 'Pinpin'
    PACKAGES_NAME: str = 'Packages'
    USER_ICON_NAME: str = 'user_icon.png'
    
    
    # PINPIN ----------------------------------------------------------------------------------------------------
    @classmethod
    def pinpin_path(cls) -> Path:
        return cls.find_package_path(cls.ROOT_NAME)
    
    
    @classmethod
    def packages_path(cls) -> Path:
        return cls.pinpin_path().joinpath(cls.PACKAGES_NAME)
    
    
    @classmethod
    def project_files_path(cls) -> Path:
        return cls.pinpin_path().joinpath('ProjectFiles')
    
    
    @classmethod
    def pinpin_icons_path(cls) -> Path:
        return cls.project_files_path().joinpath('Icons')
    
    
    @classmethod
    def pinpin_icon_path(cls) -> Path:
        return cls.pinpin_icons_path().joinpath('pinpin_icon.ico')
    
    
    @classmethod
    def current_version(cls) -> str:
        return cls.prefs_dest().VERSION_JSONFILE.get_value('version')
    
    
    # USER ------------------------------------------------------------------------------------------------------
    @classmethod
    def username(cls) -> str:
        return os.getenv('USERNAME')
    
    
    @classmethod
    def user_dir(cls) -> Path:
        return Path.home()
    
    
    @classmethod
    def documents_dir(cls) -> Path:
        return Path.home().joinpath('Documents')
    
    
    # PROJECT INFOS ---------------------------------------------------------------------------------------------
    @classmethod
    def project_data_paths(cls) -> ProjectDataPaths:
        
        return ProjectDataPaths(
            PROJECT_PATH = cls.pref_infos(root=Root.DEST).CURRENT_PROJECT
        )
    
    
    @classmethod
    def project_data(cls) -> ProjectData:
        
        project_data: ProjectDataPaths = cls.project_data_paths()
        
        return ProjectData(
            FILE_DATA_DICT = project_data.FILE_DATA_JSONFILE.json_to_dict(),
            PREFIX = project_data.PREFIX_JSONFILE.get_value('prefix')
        )
        
    
    @classmethod
    def current_project_path(cls) -> Path:
        
        return Path(cls.prefs_dest().CURRENT_PROJECT_JSONFILE.get_value('current_project'))
    
    
    # PREFERENCES INFOS & PATHS ---------------------------------------------------------------------------------
    @classmethod
    def pref_infos(cls, root: Root = Root.DEST) -> PreferencesInfos:
                
        prefs_paths: PreferencesPaths = cls.prefs_paths(root = root)
        
        return PreferencesInfos(
            CURRENT_PROJECT = prefs_paths.CURRENT_PROJECT_JSONFILE.get_value('current_project'),
            LAST_PATHS = prefs_paths.MEMO_PATH_JSONFILE.get_value('last_paths'),
            RECENT_FILES = prefs_paths.RECENT_FILES_JSONFILE.get_value('recent_files'),
            NUM_FILES = prefs_paths.UI_PREFS_JSONFILE.get_value('num_files'),
            REVERSE_SORT_FILES = prefs_paths.UI_PREFS_JSONFILE.get_value('reverse_sort_files'),
            VERSION = prefs_paths.VERSION_JSONFILE.get_value('version')
        )
        
    
    @classmethod
    def prefs_root(cls, root: Root = Root.DEST) -> Path:
        
        if root == Root.DEST:
            return cls.user_dir().joinpath('.pinpin')
        
        if root == Root.SOURCE:
            return cls.pinpin_path().joinpath('.pinpin')
    
    
    @classmethod
    def prefs_paths(cls, root: Root = Root.DEST) -> PreferencesPaths:
        
        if root == Root.DEST:
            return PreferencesPaths(
                USER_PREFS_ROOT = cls.user_dir().joinpath('.pinpin')
            )
            
        if root == Root.SOURCE:
            return PreferencesPaths(
                USER_PREFS_ROOT = cls.pinpin_path().joinpath('.pinpin')
            )
    
    
    @classmethod
    def prefs_source(cls) -> PreferencesPaths:
        return cls.prefs_paths(root = Root.SOURCE)
    
    
    @classmethod
    def prefs_dest(cls) -> PreferencesPaths:
        return cls.prefs_paths(root = Root.DEST)
    
    
    @classmethod
    def today_log_filepath(cls) -> Path:
        return cls.prefs_dest().LOGS_DIRPATH.joinpath(f'{datetime.now().strftime("%Y-%m-%d")}_{cls.username()}.log')
    
    
    # SOFTWARE PATHS ---------------------------------------------------------------------------------------------
    @classmethod
    def houdini_infos(cls) -> SoftwarePaths:
        
        integration_path: Path = cls.packages_path().joinpath('apps', 'houdini', 'integration')
        pinpin_menu_source_path : Path = integration_path.joinpath('pinpin.radialmenu')
        pinpin_shelf_source_path: Path = integration_path.joinpath('pinpin.shelf')
        
        preferences_path: Path = cls.find_directory(parent_directory=cls.documents_dir(), directory_string='houdini')
        pinpin_menu_dest_path: Path = preferences_path.joinpath('radialmenu', 'pinpin.radialmenu')
        pinpin_shelf_dest_path: Path = preferences_path.joinpath('toolbar', 'pinpin.shelf')
        
        return SoftwarePaths(
            INTEGRATION_PATH=integration_path,
            PINPIN_MENU_SOURCE_PATH=pinpin_menu_source_path,
            PINPIN_SHELF_SOURCE_PATH=pinpin_shelf_source_path,
            
            PREFERENCES_PATH=preferences_path,
            PINPIN_MENU_DEST_PATH=pinpin_menu_dest_path,
            PINPIN_SHELF_DEST_PATH=pinpin_shelf_dest_path
        )
        
        
    @classmethod
    def maya_infos(cls) -> SoftwarePaths:
        
        integration_path: Path = cls.packages_path().joinpath('apps', 'maya_app', 'integration')
        pinpin_menu_source_path : Path = integration_path.joinpath('menu_pinpinMenu.mel')
        pinpin_shelf_source_path: Path = integration_path.joinpath('shelf_Pinpin.mel')
        
        preferences_path: Path = cls.documents_dir().joinpath('maya')
        preferences_path: Path = next((preferences_path.joinpath(dir) for dir in os.listdir(preferences_path) if cls.is_four_digits(dir)), '2024')
        pinpin_menu_dest_path: Path = preferences_path.joinpath('prefs', 'markingMenus', 'menu_pinpinMenu.mel')
        pinpin_shelf_dest_path: Path = preferences_path.joinpath('prefs', 'shelves', 'shelf_Pinpin.mel')
        
        return SoftwarePaths(
            INTEGRATION_PATH=integration_path,
            PINPIN_MENU_SOURCE_PATH=pinpin_menu_source_path,
            PINPIN_SHELF_SOURCE_PATH=pinpin_shelf_source_path,
            
            PREFERENCES_PATH=preferences_path,
            PINPIN_MENU_DEST_PATH=pinpin_menu_dest_path,
            PINPIN_SHELF_DEST_PATH=pinpin_shelf_dest_path
        )
    
    
    # USEFUL FUNCS -----------------------------------------------------------------------------------------------
    @staticmethod
    def find_package_path(package_name: str) -> Path:
        current_path = os.path.abspath(__file__)
        while current_path:
            current_dir, dirname = os.path.split(current_path)
            if dirname == package_name:
                return Path(current_path)
            current_path = current_dir
    
        
    @staticmethod
    def find_directory(parent_directory: Path, directory_string: str, exclude_strings = [], exe=False) -> Path:
        """
        Searches for a directory or executable file in a given parent directory based on a string pattern.

        Parameters
        ----------
        parent_directory : Path
            The directory where the search will be performed.
        directory_string : str
            The string pattern to match the directory or file names.
        exclude_strings : list, optional
            A list of strings to exclude from the search results. Default is an empty list.
        exe : bool, optional
            If True, searches for executable files (.exe); otherwise, searches for directories. Default is False.

        Returns
        -------
        Path
            The path to the matching directory or executable file.
        """
        
        for dir in parent_directory.iterdir():
            dir_name: str = dir.name
            if not dir_name.startswith(directory_string):
                continue
            if dir_name in exclude_strings:
                    continue
            if exe:
                if dir_name.endswith('.exe'):
                    return dir
            else:
                return dir
            
    
    @staticmethod
    def is_four_digits(string: str) -> bool:
        return bool(re.match(r'^\d{4}$', string))
    
    
    @staticmethod
    def find_root_dirpath(file_path: Path, project_path: Path) -> Path:
        
        parents = list(file_path.parents)
        
        for parent in parents:
            if parent.parent == project_path:
                return parent

        return None
    

def main() -> None:
    
    print('# PINPIN ----------------------------------------------------------------------------------------------------')
    print(f'Pinpin root path: {Core.pinpin_path()}')
    print(f'Packages path: {Core.packages_path()}')
    
    print('# USER ------------------------------------------------------------------------------------------------------')
    print(f'Username: {Core.username()}')
    print(f'Userdir: {Core.user_dir()}')
    print(f'Documents dir: {Core.documents_dir()}')
    
    print('# PREFERENCES INFOS & PATHS ---------------------------------------------------------------------------------')
    print(Core.prefs_source().apps_json_path)
    print(Core.prefs_dest().apps_json_path)
    print(f'Cliked items: {Core.pref_infos(root = Root.SOURCE).clicked_items}')
    print(f'Current project: {Core.pref_infos(root = Root.SOURCE).current_project}')
    print(f'Num files: {Core.pref_infos(root = Root.SOURCE).num_files}')
    print(f'Recent files: {Core.pref_infos(root = Root.SOURCE).recent_files}')
    print(f'Reverse sort files: {Core.pref_infos(root = Root.SOURCE).reverse_sort_files}')
    print(f'Version: {Core.pref_infos(root = Root.SOURCE).version}')
    print(f'FakeProject path: {Core.prefs_paths(root = Root.SOURCE).fake_project_path}')
    
    print('# SOFTWARE PATHS --------------------------------------------------------------------------------------------')
    print(Core.houdini_infos())
    print(Core.maya_infos())


if __name__ == '__main__':
    main()
