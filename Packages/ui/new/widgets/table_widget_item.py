from pathlib import Path
from typing import Union
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTableWidgetItem


class TableWidgetItem(QTableWidgetItem):
    
    
    def __init__(self, path: Path, text: str = '', size: Union[int, None] = None):
        super(TableWidgetItem, self).__init__()
    
        self._pipeline_path: Path = path
        
        self.setTextAlignment(Qt.AlignCenter)
        if text:
            self.setText(text)
            if size:
                self.setFont(QFont(QFont().family(), size))
                
        self.setToolTip(
            f'<span style="font-size: 14px; background-color: white; color: black; border: 0px transparent;">{self.pipeline_name}</span>'
        )
    
    
    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path) -> None:
        self._pipeline_path = path
    
    
    @property
    def pipeline_name(self) -> str:
        return self._pipeline_path.name if self._pipeline_path else None
