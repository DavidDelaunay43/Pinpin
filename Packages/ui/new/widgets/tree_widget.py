from pathlib import Path
from typing import Union
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QTreeWidget


class TreeWidget(QTreeWidget):
    
    
    def __init__(self):
        super(self, TreeWidget).__init__()
        
        self._pipeline_path: Union[Path, None] = None
        
        self.setMinimumWidth(250)
        self.setHeaderHidden(True)
        self.setTextElideMode(Qt.ElideNone)
        self.setAnimated(True)
        self.header().setVisible(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("font-size: 14px;")
        self.setIconSize(QSize(35, 35))
        
        
    @property
    def pipeline_path(self) -> Union[Path, None]:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
        

    @property
    def pipeline_name(self) -> Union[str, None]:
        return self._pipeline_path.name if self._pipeline_path else None
