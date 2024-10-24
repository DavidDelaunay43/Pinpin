import json
from pathlib import Path
from typing import Union


class AppFinder:
    """
    A class to locate installed 3D and digital content creation applications on the system (Windows).
    This class allows for customization of the directories and can generate a JSON file with the paths 
    to applications and their preferences.
    
    Attributes
    ----------
    _program_files : Path
        The default path to 'Program Files' directory.
    _user_dir : Path
        The default path to the user's home directory.
    _documents_dir : Path
        The path to the 'Documents' directory of the user.
    APPS : tuple
        A tuple containing the names of supported applications.
    app_dict : dict
        A dictionary containing application details, including paths and preferences.
    """
    
    
    _program_files: Path = Path('C:/Program Files')
    _user_dir: Path = Path.home()
    _documents_dir: Path = _user_dir.joinpath('Documents')
    APPS: tuple = 'blender', 'it', 'krita', 'houdini', 'maya', 'mari', 'nuke', 'photoshop', 'substance_designer', 'substance_painter', 'zbrush'
    app_dict: dict = {app: {'path': None, 'pref': None, 'python_path': None, 'file': None} for app in APPS}
    
    
    @classmethod
    def show_app_dict(cls) -> None:
        print(json.dumps(cls.app_dict, indent=4))
    
    
    @classmethod
    def get_user_dir(cls) -> Path:
        """
        Returns the path to the user's home directory.

        Returns
        -------
        Path
            The path to the user's home directory.
        """
        
        return cls._user_dir
    
    
    @classmethod
    def set_user_dir(cls, new_path: Union[str, Path]) -> None:
        """
        Updates the user's home directory path and recalculates the path to the 'Documents' directory.

        Parameters
        ----------
        new_path : Union[str, Path]
            The new path to set as the user's home directory.
        """
        
        cls._user_dir = Path(new_path) if not isinstance(new_path, Path) else new_path
        cls._documents_dir = cls._user_dir.joinpath('Documents')
        
        
    @classmethod
    def get_program_files_dir(cls) -> Path:
        """
        Returns the path to the 'Program Files' directory.

        Returns
        -------
        Path
            The path to the 'Program Files' directory.
        """
        
        return cls._program_files
    
    
    @classmethod
    def set_program_files_dir(cls, new_path: Union[str, Path]) -> None:
        """
        Updates the 'Program Files' directory path.

        Parameters
        ----------
        new_path : Union[str, Path]
            The new path to set as the 'Program Files' directory.
        """
        
        cls._program_files = Path(new_path) if not isinstance(new_path, Path) else new_path

    
    @classmethod
    def find_3d_applications(cls) -> None:
        """
        Populates the `app_dict` with paths and preference directories for 3D and content creation applications.
        The method searches for Blender, Krita, Houdini, Mari, Maya, Nuke, Photoshop, and ZBrush, 
        and updates their paths and preference directories in `app_dict`.
        """
        
        cls.app_dict['blender']['path'] = cls.find_blender()
        cls.app_dict['krita']['path'] = cls.find_krita()
        cls.app_dict['houdini']['path'] = cls.find_houdini()
        #cls.app_dict['mari']['path'] = cls.find_mari()
        cls.app_dict['maya']['path'] = cls.find_maya()
        cls.app_dict['nuke']['path'] = cls.find_nuke()
        cls.app_dict['photoshop']['path'] = cls.find_photoshop()
        cls.app_dict['zbrush']['path'] = cls.find_zbrush()
        
        cls.app_dict['houdini']['pref'] = cls.find_houdini_pref()
        #cls.app_dict['mari']['pref'] = cls.find_mari_pref()
        cls.app_dict['maya']['pref'] = cls.find_maya_pref()
        cls.app_dict['nuke']['pref'] = cls.find_nuke_pref()
        

    @classmethod
    def write_json_file(cls, json_filepath: Union[str, Path]):
        """
        Writes the application dictionary (`app_dict`) to a JSON file.

        Parameters
        ----------
        json_filepath : Union[str, Path]
            The path to the JSON file where the application data will be saved.
        """
        
        with open(json_filepath, 'w', encoding='utf-8') as json_file:
            json.dump(cls.app_dict, json_file, indent=4, ensure_ascii=False)
        
    
    @staticmethod
    def json_is_empty(json_filepath: Union[str, Path]) -> bool:
        
        with open(json_filepath, 'r', encoding='utf-8') as json_file:
            app_dict: dict = json.load(json_file)
        
        return all(
            all(v is None for v in value.values())
            for value in app_dict.values()
        )
    
    
    @staticmethod
    def find_directory(parent_directory: Path, directory_string: str, exclude_strings: list[str] = [], exe: bool = False) -> Union[Path, None]:
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
        
    
    @classmethod  
    def find_blender(cls) -> Union[str, None]:
        exe: str = 'blender.exe'
        parent_dir: Path = cls._program_files.joinpath('Blender Foundation')
        exe_parent_path: Union[Path, None] = cls.find_directory(parent_directory=parent_dir, directory_string='Blender ')
        return str(exe_parent_path.joinpath(exe)) if exe_parent_path else None
        
    
    @classmethod
    def find_krita(cls) -> Union[str, None]:
        exe: str = 'krita.exe'
        exe_path: Path = cls._program_files.joinpath('Krita (x64)', 'bin', exe)
        return str(exe_path) if exe_path.exists() else None
    
    
    @classmethod
    def find_houdini(cls) -> Union[str, None]:
        parent_dir: Path = cls._program_files.joinpath('Side Effects Software')
        exe_parent_path: Union[Path, None] = cls.find_directory(parent_directory=parent_dir, directory_string='Houdini', exclude_strings=['Houdini Engine', 'Houdini Server'])
        return str(exe_parent_path.joinpath('bin', 'houdini.exe')) if exe_parent_path else None
    
    
    @classmethod
    def find_mari(cls) -> Union[str, None]:
        parent_dir: Union[Path, None] = cls.find_directory(parent_directory=cls._program_files, directory_string='Mari')
        return str(cls.find_directory(parent_directory=parent_dir.joinpath('Bundle', 'bin')), directory_string='Mari') if parent_dir else None
    
    
    @classmethod
    def find_maya(cls) -> Union[str, None]:
        parent_dir: Path = cls._program_files.joinpath('Autodesk')
        exe_parent_dir: Union[Path, None] = cls.find_directory(parent_directory=parent_dir, directory_string='Maya')
        return str(exe_parent_dir.joinpath('bin', 'maya.exe')) if exe_parent_dir else None
    
    
    @classmethod
    def find_nuke(cls) -> Union[str, None]:
        parent_dir: Path = cls.find_directory(parent_directory=cls._program_files, directory_string='Nuke')
        return str(cls.find_directory(parent_directory=parent_dir, directory_string='Nuke', exe=True)) if parent_dir else None
    
    
    @classmethod
    def find_photoshop(cls) -> Union[str, None]:
        parent_dir: Path = cls._program_files.joinpath('Adobe')
        exe_parent_path: Union[Path, None] = cls.find_directory(parent_directory=parent_dir, directory_string='Adobe Photoshop ')
        return str(exe_parent_path.joinpath('Photoshop.exe')) if exe_parent_path else None
    
    
    @classmethod
    def find_zbrush(cls) -> Union[str, None]:
        exe_parent_path: Union[Path, None] = cls.find_directory(parent_directory=cls._program_files, directory_string='Maxon ZBrush ')
        return str(exe_parent_path.joinpath('ZBrush.exe')) if exe_parent_path else None


    @classmethod
    def find_houdini_pref(cls) -> Union[str, None]:
        path: Union[Path, None] = cls.find_directory(parent_directory=cls._documents_dir, directory_string='houdini')
        return str(path) if path.exists() else None
    
    
    @classmethod
    def find_maya_pref(cls) -> Union[str, None]:
        path: Union[Path, None] = cls.find_directory(parent_directory=cls._documents_dir, directory_string='maya')
        return str(path) if path and path.exists() else None
    
    
    @classmethod
    def find_mari_pref(cls) -> Union[str, None]:
        path: Path = cls._user_dir.joinpath('.mari')
        return str(path) if path and path.exists() else None
    
    
    @classmethod
    def find_nuke_pref(cls) -> Union[str, None]:
        path: Path = cls._user_dir.joinpath('.nuke')
        return str(path) if path and path.exists() else None


def main() -> None:
    print(f'User directory: {AppFinder.get_user_dir()}')
    print(f'Program Files directory: {AppFinder.get_program_files_dir()}')
    print(f'Default app dict:')
    AppFinder.show_app_dict()
    AppFinder.find_3d_applications()
    print(f'Updated app dict:')
    AppFinder.show_app_dict()
    #AppFinder.write_json_file(json_filepath='tmp.json')
        

if __name__ == '__main__':
    main()
