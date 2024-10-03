from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
from typing import Union, Literal
from Packages.utils.core import Core


@dataclass
class FileInfo:
    
    file_path: Union[str, Path]
    
    def __post_init__(self):
        
        self._name: str = self.file_path.name if isinstance(self.file_path, Path) else os.path.basename(self.file_path)
        self._size: int = os.path.getsize(self.file_path)
        self._format_size: str = self.format_size()
        self._last_time: str = self.get_last_date_time()
        self._last_user: str = self.get_data('comment')
        self._comment: str = self.get_data('user')
        
    
    @property
    def size(self) -> int:
        return self._size
    
    
    @property
    def format_size(self) -> str:
        return self._format_size
    
    
    @property
    def last_time(self) -> str:
        return self._last_time
    
    
    @property
    def last_user(self) -> str:
        return self._last_user
    
    
    @property
    def comment(self) -> str:
        return self._comment
        
        
    def info_format(self) -> str:
        """
        Example:
        
        d.delaunay
        03/04/2024
        10:33
        10.57 Mo
        """
        
        return f'{self._last_user}\n{self._last_time}\n{self._format_size}'
    
    
    def format_size(self) -> str:
        
        size_bytes: int = self._size
        
        if size_bytes == 0:
            return '0 o'
        
        suffix = ['o', 'Ko', 'Mo', 'Go', 'To', 'Po', 'Eo', 'Zo', 'Yo']
        
        i = 0
        while size_bytes >= 1024 and i < len(suffix)-1:
            size_bytes /= 1024.0
            i += 1
        
        return f'{size_bytes:.2f} {suffix[i]}'
    
    
    def get_data(self, data: Literal['user', 'comment']) -> str:
        
        file_info_dict: dict = Core.project_data().FILE_DATA_DICT
        
        if not self.file_path in file_info_dict.keys():
            return ''
        
        return file_info_dict.get(self.file_path.get(data), '')

    
    def get_last_date_time(self) -> str:
        return datetime.fromtimestamp(os.stat(self.file_path).st_mtime).strftime('%d-%m-%Y\n%H:%M')
    
    
    def external_increment(self):
        ...
