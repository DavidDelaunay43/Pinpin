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
        
        cls.app_dict['blender']['path'] = str(cls.find_blender())
        cls.app_dict['krita']['path'] = str(cls.find_krita())
        cls.app_dict['houdini']['path'] = str(cls.find_houdini())
        cls.app_dict['mari']['path'] = str(cls.find_mari())
        cls.app_dict['maya']['path'] = str(cls.find_maya())
        cls.app_dict['nuke']['path'] = str(cls.find_nuke())
        cls.app_dict['photoshop']['path'] = str(cls.find_photoshop())
        cls.app_dict['zbrush']['path'] = str(cls.find_zbrush())
        
        cls.app_dict['houdini']['pref'] = str(cls.find_houdini_pref())
        cls.app_dict['mari']['pref'] = str(cls.find_mari_pref())
        cls.app_dict['maya']['pref'] = str(cls.find_maya_pref())
        cls.app_dict['nuke']['pref'] = str(cls.find_nuke_pref())
        

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
        
    
    @classmethod  
    def find_blender(cls) -> Path:
        exe: str = 'blender.exe'
        parent_dir: Path = cls._program_files.joinpath('Blender Foundation')
        dir_string: str = 'Blender '
        return cls.find_directory(parent_directory=parent_dir, directory_string=dir_string).joinpath(exe)
        
    
    @classmethod
    def find_krita(cls) -> Path:
        exe: str = 'krita.exe'
        return cls._program_files.joinpath('Krita (x64)', 'bin', exe)
    
    
    @classmethod
    def find_houdini(cls) -> Path:
        exe: str = 'houdini.exe'
        parent_dir: Path = cls._program_files.joinpath('Side Effects Software')
        dir_string: str = 'Houdini'
        return cls.find_directory(parent_directory=parent_dir, directory_string=dir_string, exclude_strings=['Houdini Engine', 'Houdini Server']).joinpath('bin', exe)
    
    
    @classmethod
    def find_mari(cls) -> Path:
        mari: str = 'Mari'
        parent_dir: Path = cls._program_files.joinpath(cls.find_directory(parent_directory=cls._program_files, directory_string=mari), 'Bundle', 'bin')
        return cls.find_directory(parent_directory=parent_dir, directory_string=mari)
    
    
    @classmethod
    def find_maya(cls) -> Path:
        exe: str = 'maya.exe'
        parent_dir: Path = cls._program_files.joinpath('Autodesk')
        dir_string: str = 'Maya'
        return cls.find_directory(parent_directory=parent_dir, directory_string=dir_string).joinpath('bin', exe)
    
    
    @classmethod
    def find_nuke(cls) -> Path:
        nuke: str = 'Nuke'
        parent_dir: Path = cls._program_files.joinpath(cls.find_directory(parent_directory=cls._program_files, directory_string=nuke))
        return cls.find_directory(parent_directory=parent_dir, directory_string=nuke, exe=True)
    
    
    @classmethod
    def find_photoshop(cls) -> Path:
        exe: str = 'Photoshop.exe'
        parent_dir: Path = cls._program_files.joinpath('Adobe')
        dir_string: str = 'Adobe Photoshop '
        return cls.find_directory(parent_directory=parent_dir, directory_string=dir_string).joinpath(exe)
    
    
    @classmethod
    def find_zbrush(cls) -> Path:
        exe: str = 'ZBrush.exe'
        return cls._program_files.joinpath(cls.find_directory(parent_directory=cls._program_files, directory_string='Maxon ZBrush ')).joinpath(exe)


    @classmethod
    def find_houdini_pref(cls) -> str:
        return cls._documents_dir.joinpath(cls.find_directory(parent_directory=cls._documents_dir, directory_string='houdini'))
    
    
    @classmethod
    def find_maya_pref(cls) -> Path:
        return cls._documents_dir.joinpath(cls.find_directory(parent_directory=cls._documents_dir, directory_string='maya'))
    
    
    @classmethod
    def find_mari_pref(cls) -> Path:
        return cls._user_dir.joinpath('.mari')
    
    
    @classmethod
    def find_nuke_pref(cls) -> Path:
        return cls._user_dir.joinpath('.nuke')


def main() -> None:
    print(f'User directory: {AppFinder.get_user_dir()}')
    print(f'Program Files directory: {AppFinder.get_program_files_dir()}')
    print(f'Default app dict:')
    AppFinder.show_app_dict()
    AppFinder.find_3d_applications()
    print(f'Updated app dict:')
    AppFinder.show_app_dict()
    AppFinder.write_json_file(json_filepath='tmp.json')
        

if __name__ == '__main__':
    main()
