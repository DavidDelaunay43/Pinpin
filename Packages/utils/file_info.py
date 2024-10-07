from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
import re
from typing import Literal, Union
from Packages.utils.core import Core


@dataclass
class FileInfo:
    
    _pipeline_path: Path
    
    def __post_init__(self):
        
        self._size: int = os.path.getsize(self._pipeline_path)
        self._format_size: str = self.format_size()
        self._last_time: str = self.get_last_date_time()
        self._last_user: str = self.get_data('comment')
        self._comment: str = self.get_data('user')
        self._version: str = self.get_version()
        
        
    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
        
    
    @property
    def pipeline_name(self) -> str:
        return self._pipeline_path.name
        
    
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
    def last_user(self) -> Union[str, None]:
        return self._last_user if self._last_user else None
    
    
    @property
    def comment(self) -> Union[str, None]:
        return self._comment if self._comment else None
    
    
    @property
    def version(self) -> Union[str, None]:
        return self._version
        
    
    @property    
    def info_format(self) -> str:
        """
        Example:
        
        d.delaunay
        03/04/2024
        10:33
        10.57 Mo
        """
        
        return f'{self.last_user}\n{self._last_time}\n{self._format_size}' if self.last_user else f'\n{self._last_time}\n{self._format_size}'
    
    
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
        
        if not self._pipeline_path in file_info_dict.keys():
            return ''
        
        return file_info_dict.get(self._pipeline_path.get(data), '')

    
    def get_last_date_time(self) -> str:
        return datetime.fromtimestamp(os.stat(self._pipeline_path).st_mtime).strftime('%d-%m-%Y\n%H:%M')
    
    
    def get_version(self) -> str:
        
        return self.find_three_digits()
        
        
    def find_three_digits(self) -> Union[str, None]:
        
        match_string: Union[re.Match[str], None] = re.search('\d{3}', self.pipeline_name)
        return match_string.group() if match_string else None
    
    
    def external_increment(self):
        ...
