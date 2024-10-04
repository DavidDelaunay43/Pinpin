from pathlib import Path
from typing import Union
from PySide2.QtWidgets import *


class CheckableButton(QPushButton):
    
    
    def __init__(self, path: Path, text: str = '', minimum_size: list = [60, 35]) -> None:
        super(CheckableButton, self).__init__(text)
        
        self.setCheckable(True)
        self.setMinimumSize(*minimum_size)
        self.setObjectName('checkable_button')
        self._pipeline_path: Union[Path, None] = path


    @property
    def pipeline_path(self) -> Union[Path, None]:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path


    @property
    def pipeline_name(self) -> Union[str, None]:
        return self._pipeline_path.name if self._pipeline_path else None
