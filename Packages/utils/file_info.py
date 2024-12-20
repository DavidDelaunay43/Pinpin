from datetime import datetime
import os
from pathlib import Path
import re
import shutil
from typing import Literal, Union
from Packages.utils.core import Core
from Packages.utils.logger import Logger


class FileInfo:


    def __init__(self, path: Union[Path, str]) -> None:

        self._pipeline_path: Path = path if isinstance(path, Path) else Path(path)
        self._size: int = self._pipeline_path.stat().st_size
        self._format_size: str = self.format_size()
        self._last_time: str = self.get_last_date_time()
        self._last_user: str = self.get_data('user')
        self._comment: str = self.get_data('comment')
        self._version: str = self.get_version()
        self.NEXT_PIPELINE_PATH: Path = self._find_next_filepath()
        self.NEXT_PIPELINE_NAME: str = self.NEXT_PIPELINE_PATH.name if self.NEXT_PIPELINE_PATH else None
    

    @property
    def EXT(self) -> str:
        return self.pipeline_path.suffix


    @property
    def WORDS(self) -> list[str]:
        return self.pipeline_name.split('.')[0].split('_')


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
    def parent_dirpath(self) -> Path:
        return self._pipeline_path.parent
        
    
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
    def extension(self) -> Union[str, None]:
        return self._pipeline_path.suffix if self._pipeline_path else None
        
        
    @property
    def next_pipeline_path(self) -> Path:
        return self._find_next_filepath()
    
    
    @property
    def base_name(self) -> str:
        return self.pipeline_name.split(self.version)[0]
    
    
    @property
    def same_files(self) -> list[Path]:
        return [
            file_path
            for file_path in self.parent_dirpath.iterdir()
            if self.base_name in file_path.name
        ]
    
    
    @property
    def same_files_count(self) -> int:
        return len(self.same_files)
        
    
    @property    
    def info_format(self) -> str:
        """
        Example:
        
        d.delaunay
        03/04/2024
        10:33
        10.57 Mo
        .mb
        """
        if self.last_user:
            return f'{self.last_user}\n{self._last_time}\n{self._format_size}\n{self.extension}'
        else: 
            return f'\n{self._last_time}\n{self._format_size}\n{self.extension}'
    
    
    @property
    def preview_image_path(self) -> Union[Path, None]:
        return self._find_preview_image()
    
    
    def format_size(self) -> str:
        
        size_bytes: int = self.size
        
        if size_bytes == 0:
            return '0 o'
        
        suffix = 'o', 'Ko', 'Mo', 'Go', 'To', 'Po', 'Eo', 'Zo', 'Yo'
        
        i = 0
        while size_bytes >= 1024 and i < len(suffix)-1:
            size_bytes /= 1024.0
            i += 1
        
        return f'{size_bytes:.2f} {suffix[i]}'
    
    
    def get_data(self, data: Literal['comment', 'user']) -> str:
        
        file_info_dict: dict = Core.project_data_paths().FILE_DATA_JSONFILE.json_to_dict()
        
        if not str(self._pipeline_path) in file_info_dict.keys():
            return ''
        
        return file_info_dict[str(self._pipeline_path)][data]

    
    def get_last_date_time(self) -> str:
        return datetime.fromtimestamp(os.stat(self._pipeline_path).st_mtime).strftime('%d-%m-%Y\n%H:%M')
    
    
    def get_version(self) -> str:
        if '_P.' in self.pipeline_name:
            version = self.find_three_digits()
            return self.pipeline_name.split('_')[-3] # if not version else f'{self.pipeline_name.split("_")[-4]}\n{version}'
        return self.find_three_digits()
        
        
    def find_three_digits(self) -> Union[str, None]:
        
        match_string: Union[re.Match[str], None] = re.findall('\d{3}', self.pipeline_name)
        return match_string[-1] if match_string else None
    
    
    def _find_next_filepath(self) -> Union[Path, None]:
        
        if not self.find_three_digits():
            return
        
        current_version: int = int(self.version)
        number_of_versions: int = self.same_files_count
        
        if current_version==number_of_versions or current_version>number_of_versions or current_version+1==number_of_versions:
            new_version = current_version+1

        else:
            new_version = int(re.findall('\d{3}', self.same_files[-1].name)[-1]) +1
        
        #new_file_name: str = self.pipeline_name.replace(self.version, f'{new_version:03}')
        new_file_name: str = re.sub(r'(\d{3})(?!.*\d{3})', f'{new_version:03}', self.pipeline_name)
        return self.parent_dirpath.joinpath(new_file_name)
    
    
    def external_increment(self):
        shutil.copy(self.pipeline_path, self.next_pipeline_path)
        Core.project_data_paths().FILE_DATA_JSONFILE.set_value(str(self.NEXT_PIPELINE_PATH), {'comment': None, 'user': Core.username()})
        return self.NEXT_PIPELINE_PATH
    
    
    def _find_preview_image(self) -> Union[Path, None]:
        preview_image_path: Path = Core.project_data_paths().PREVIEW_DIRPATH.joinpath(f'{self.pipeline_name}.jpg')
        return preview_image_path if preview_image_path.exists() else None
