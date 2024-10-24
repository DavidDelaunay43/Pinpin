from pathlib import Path
from typing import Union
from PySide2.QtWidgets import QLineEdit


class StatusBar(QLineEdit):
    
    
    def __init__(self, parent=None, path: Union[Path, None] = None):
        super(StatusBar, self).__init__(parent)
        
        self._pipeline_path: Union[Path, None] = path
        
        self.setReadOnly(True)
        self.setMinimumHeight(30)
        self.setStyleSheet('font-size: 14px; color: rgb(220, 220, 220)')
        
        
    @property
    def pipeline_path(self) -> Union[Path, None]:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
        self.setText(str(path))
    
    
    @property
    def pipeline_name(self) -> Union[str, None]:
        return self._pipeline_path.name if self._pipeline_path else None
