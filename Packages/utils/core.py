import os
from pathlib import Path
from Packages.utils.json_file import JsonFile


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
    
    # PINPIN
    def pinpin_path(self) -> Path:
        return self.find_package_path(self.ROOT_NAME)
    
    
    def packages_path(self) -> Path:
        return self.pinpin_path().joinpath(self.PACKAGES_NAME)
    
    
    # USER
    def username(self) -> str:
        return f'{os.getenv("USERNAME")}'
    
    
    def user_dir(self) -> Path:
        return Path(os.path.expanduser("~"))
    
    
    # PREFERENCES
    def user_prefs(self) -> Path:
        return self.user_dir().joinpath('.pinpin')
    
    
    def logs_path(self) -> Path:
        return self.user_prefs().joinpath('logs')
    
    
    def apps_json_path(self) -> Path:
        return self.user_dir().joinpath('apps.json')
    
    
    def clicked_items_json_path(self) -> Path:
        return self.user_dir().joinpath('clicked_items.json')
    
    
    def current_project_json_path(self) -> Path:
        return self.user_dir().joinpath('current_project.json')
    
    
    def recent_files_json_path(self) -> Path:
        return self.user_dir().joinpath('recent_files.json')
    
    
    def ui_prefs_json_path(self) -> Path:
        return self.user_dir().joinpath('ui_prefs.json')
    
    
    def version_json_path(self) -> Path:
        return self.user_dir().joinpath('version.json')
    
    
    def apps_json_file(self) -> JsonFile:
        return JsonFile(self.apps_json_path())
    
    
    def clicked_items_json_file(self) -> JsonFile:
        return JsonFile(self.clicked_items_json_path())
    
    
    def current_project_json_file(self) -> JsonFile:
        return JsonFile(self.clicked_items_json_path())
    
    
    def recent_files_json_file(self) -> JsonFile:
        return JsonFile(self.recent_files_json_path())
    
    
    def ui_prefs_json_file(self) -> JsonFile:
        return JsonFile(self.ui_prefs_json_path())
    
    
    def version_json_file(self) -> JsonFile:
        return JsonFile(self.version_json_path)


    def current_project_path(self) -> Path:
        return self.current_project_json_file().get_value('current_project')
        
        
    def recent_files_list(self) -> list:
        return self.recent_files_json_file().get_value('recent_files')
    
    
    def version(self) -> str:
        return self.version_json_file().get_value('version')
    
    
    def num_files(self) -> int:
        return self.ui_prefs_json_file().get_value('num_files')
    
    
    def reverse_sort_files(self) -> bool:
        return self.ui_prefs_json_file().get_value('reverse_sort_file')


    def find_package_path(self, package_name: str) -> Path:
        current_path = os.path.abspath(__file__)
        while current_path:
            current_dir, dirname = os.path.split(current_path)
            if dirname == package_name:
                return Path(current_path)
            current_path = current_dir
