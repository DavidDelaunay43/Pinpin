from pathlib import Path
from typing import Union
from PySide2.QtWidgets import QLabel


class StatusBar(QLabel):
    
    
    def __init__(self, path: Union[Path, None] = None):
        super(StatusBar, self).__init__()
        
        self._pipeline_path: Union[Path, None] = path
        
        self.setStyleSheet('font-weight: bold;')
        self.setStyleSheet('font-size: 12px;')
        
        
    @property
    def pipeline_path(self) -> Union[Path, None]:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
    
    
    @property
    def pipeline_name(self) -> Union[str, None]:
        return self._pipeline_path.name if self._pipeline_path else None
