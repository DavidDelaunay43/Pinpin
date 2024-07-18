import json
from pathlib import Path


class JsonFile:
    
    
    def __init__(self, path: str | Path) -> None:
        self.PATH = Path(path)
        self.NAME = self.PATH.name
    
    
    def json_to_dict(self) -> dict:
        with open(self.PATH, 'r', encoding = 'utf-8') as file:
            dico = json.load(file)
        return dico


    def dict_to_json(self, dictionary: dict) -> None:
        with open(self.PATH, 'w', encoding = 'utf-8') as file:
            json.dump(dictionary, file, indent = 4, ensure_ascii = False)
        return
    
    
    def get_value(self, key: str) -> int | str:
        return self.json_to_dict().get(key)
    
    
    def set_value(self, key: str, value: int | str) -> None:
        dictionnary: dict = self.json_to_dict()
        dictionnary[key] = value
        self.dict_to_json(dictionnary)