from datetime import datetime
import os
from pathlib import Path
import re
from typing import Union
from Packages.utils.data_class import SoftwarePaths, PreferencesInfos, PreferencesPaths, ProjectDataPaths, ProjectData
from Packages.utils.enums import Root
from Packages.utils.json_file import JsonFile
from Packages.utils.naming import PipeRoot, PublishRoot, AssetDepartment


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
    def info_html_path(cls) -> Path:
        return cls.project_files_path().joinpath('info.html')
    
    
    @classmethod
    def pinpin_icons_path(cls) -> Path:
        return cls.project_files_path().joinpath('Icons')
    
    
    @classmethod
    def pinpin_icon_path(cls) -> Path:
        return cls.pinpin_icons_path().joinpath('pinpin_icon.ico')
    

    @classmethod
    def user_icon(cls) -> Path:
        return cls.pinpin_icons_path().joinpath(cls.USER_ICON_NAME)
    
    
    @classmethod
    def icon_path(cls, icon_name: str) -> Path:
        return cls.pinpin_icons_path().joinpath(icon_name)
    
    
    @classmethod
    def pinpin_styles_path(cls) -> Path:
        return cls.project_files_path().joinpath('Styles')
    
    
    @classmethod
    def style_icons_path(cls) -> Path:
        return Core.pinpin_styles_path().joinpath('rc')
    
    
    @classmethod
    def pinpin_style_path(cls, style_file_name: str = 'biiiped.qss') -> Path:
        return cls.pinpin_styles_path().joinpath(style_file_name)
    
    
    @classmethod
    def style_sheet(cls, style_file_name: str) -> str:
        with open(cls.pinpin_styles_path().joinpath(style_file_name), 'r') as qss_file:
            return qss_file.read()
        

    @classmethod
    def workspace_mel(cls) -> Path:
        return cls.project_files_path().joinpath('Workspaces', 'workspace.mel')
    
    
    @classmethod
    def custom_style_sheet(cls) -> str:
        
        palette_dict: dict = JsonFile(cls.pinpin_palette_file_path()).json_to_dict()
        
        with open(cls.pinpin_style_path(), 'r') as qss_file:
            style_sheet: str = qss_file.read()
        style_sheet = style_sheet.replace("MAIN_COLOR", palette_dict["MAIN_COLOR"])
        style_sheet = style_sheet.replace("SECONDARY_COLOR", palette_dict["SECONDARY_COLOR"])
        style_sheet = style_sheet.replace("TERTEARY_COLOR", palette_dict["TERTEARY_COLOR"])
        style_sheet = style_sheet.replace("CUTE_COLOR", palette_dict["CUTE_COLOR"])
        style_sheet = style_sheet.replace("COLOR_4", palette_dict["COLOR_4"])
        style_sheet = style_sheet.replace("BORDER_SIZE", palette_dict["BORDER_SIZE"])
        style_sheet = style_sheet.replace("BORDER_RADIUS", palette_dict["BORDER_RADIUS"])
        
        return style_sheet
    
    
    @classmethod
    def pinpin_palette_file_path(cls) -> Path:
        return cls.pinpin_styles_path().joinpath('palette_1.json')
    
    
    @classmethod
    def current_version(cls) -> str:
        return cls.prefs_dest().VERSION_JSONFILE.get_value('version')
    
    
    # USER ------------------------------------------------------------------------------------------------------
    @classmethod
    def username(cls) -> str:
        username: Union[str, None] = JsonFile(
            cls.user_dir().joinpath('.pinpin', 'ui_prefs.json')
        ).get_value('username')

        return username if username else os.getenv('USERNAME')


    @classmethod
    def username_custom(cls) -> str:
        return JsonFile(
            cls.user_dir().joinpath('.pinpin', 'ui_prefs.json')
        ).get_value('username')
    
    
    @classmethod
    def set_username(cls, new_username: str) -> str:
        JsonFile(
            cls.user_dir().joinpath('.pinpin', 'ui_prefs.json')
        ).set_value('username', new_username if new_username else None)

    
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
    
    
    @classmethod
    def publish_path(cls) -> Path:
        return cls.current_project_path().joinpath(PipeRoot().PUBLISH)
    

    @classmethod
    def publish_asset_path(cls) -> Path:
        return cls.publish_path().joinpath(PublishRoot.ASSET)
    

    @classmethod
    def publish_sequence_path(cls) -> Path:
        return cls.publish_path().joinpath(PublishRoot.SEQUENCE)
    

    @classmethod
    def publish_shot_path(cls) -> Path:
        return cls.publish_path().joinpath(PublishRoot.SHOT)
    

    
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
            DEV_MODE = prefs_paths.UI_PREFS_JSONFILE.get_value('dev_mode'),
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
        
        try:
            integration_path: Path = cls.packages_path().joinpath('apps', 'houdini_app', 'integration')
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
        except:
            pass
        
    
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
    def find_root_dirpath(file_path: Path, project_path: Path, return_name: bool = False) -> Path:
        
        parents = list(file_path.parents)
        
        for parent in parents:
            if parent.parent == project_path:
                return parent if not return_name else parent.name

        return None


    @classmethod
    def repath_integrations(cls, path_override: str = None) -> None:

        root_path: str = str(Core.pinpin_path()) if not path_override else path_override

        maya_shelf_path: Path = Core.packages_path().joinpath(
            'apps', 'maya_app', 'integration', 'shelf_Pinpin.mel'
        )

        with open(maya_shelf_path, 'r') as file:
            file_content = file.read()
        print(file_content)


        pattern = r'(\+\s*";"\s*\+\s*\\")([^\\]+)(\\")'
    
        file_content_modified = re.sub(pattern, r'\1' + root_path + r'\3', file_content)
        print(file_content_modified)

        with open(maya_shelf_path, 'w') as file:
            file.write(file_content_modified)
    

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
