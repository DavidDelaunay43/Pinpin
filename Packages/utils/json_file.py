import json
from pathlib import Path
from typing import Union


class JsonFile:
    """
    A class to manage reading from and writing to JSON files. The class provides methods for 
    converting JSON data to a dictionary, updating values, and working with file paths.

    Attributes
    ----------
    _path : Path
        The path to the JSON file.
    _name : str
        The name of the JSON file.
    """
    
    
    def __init__(self, path: Union[str, Path]) -> None:
        self._path: Path = Path(path).absolute()
        self._name = self._path.name


    @property
    def path(self) -> Path:
        return self._path
    
    
    @path.setter
    def path(self, new_path: Union[str, Path]) -> None:
        self._path = Path(new_path) if not isinstance(new_path, Path) else new_path
        self._name = self._path.name
    
    
    @property
    def name(self) -> str:
        return self._name


    def json_to_dict(self) -> dict:
        """
        Reads the JSON file and converts it to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the JSON file content.

        Raises
        ------
        FileNotFoundError
            If the JSON file does not exist at the specified path.
        """
        
        with open(self._path, 'r', encoding='utf-8') as file:
            dico = json.load(file)
        return dico


    def dict_to_json(self, dictionary: dict) -> None:
        
        """
        Writes a dictionary to the JSON file.

        Parameters
        ----------
        dictionary : dict
            The dictionary to be written to the JSON file.
        
        Notes
        -----
        Any `Path` objects in the dictionary are automatically converted to strings.
        """
        
        dictionary = {key: str(value) if isinstance(value, Path) else value for key, value in dictionary.items()}
        with open(self._path, 'w', encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4, ensure_ascii=False)
        return
    
    
    def get_value(self, key: str, return_path: bool = False) -> Union[bool, int, float, str, list, dict, Path, None]:
        """
        Retrieves the value associated with a key from the JSON file.

        Parameters
        ----------
        key : str
            The key for which the value is to be retrieved.
        return_path : bool, optional
            If True, returns the value as a Path object if the value is a string (default is False).

        Returns
        -------
        Union[bool, int, float, str, list, dict, Path, None]
            The value associated with the key in the JSON file. If `return_path` is True and the value is a string, 
            it will be returned as a Path object.

        Raises
        ------
        KeyError
            If the key is not found in the JSON file.
        """
        
        value = self.json_to_dict().get(key)
        return Path(value) if return_path and isinstance(value, str) else value
    
    
    def set_value(self, key: str, value: Union[bool, int, float, str, list, dict, Path, None]) -> None:
        """
        Updates or adds a key-value pair in the JSON file.

        Parameters
        ----------
        key : str
            The key to be added or updated in the JSON file.
        value : Union[bool, int, float, str, list, dict, Path, None]
            The value to be assigned to the key. Path objects are converted to strings.

        Raises
        ------
        FileNotFoundError
            If the JSON file does not exist.
        """
        
        value = str(value) if isinstance(value, Path) else value
        dictionnary = self.json_to_dict()
        dictionnary[key] = value
        self.dict_to_json(dictionnary)


    def exists(self) -> bool:
        return self._path.exists()
    