from pathlib import Path
from typing import Union
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QTreeWidgetItem


class TreeWidgetItem(QTreeWidgetItem):
    
    
    def __init__(self, parent, path: Path, size: Union[list[int], None] = None) -> None:
        super(TreeWidgetItem, self).__init__(parent)
        
        self._pipeline_path: Path = path
        self.setText(0, self.pipeline_name)
        if size:
            self.setSizeHint(0, QSize(*size))
    
        
    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path) -> None:
        self._pipeline_path = path
        self.setText(0, self.pipeline_name)
    
    
    @property
    def pipeline_name(self) -> str:
        return self._pipeline_path.name if self._pipeline_path else None
