from pathlib import Path
from PySide2.QtWidgets import QListWidgetItem


class ListWidgetItem(QListWidgetItem):
    
    
    def __init__(self, parent, path: Path) -> None:
        super(ListWidgetItem, self).__init__(parent)
        
        self._pipeline_path: Path = path
        self.setText(self.pipeline_name)
        
        
    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
        self.setText(self.pipeline_name)
        
        
    @property
    def pipeline_name(self) -> str:
        return self._pipeline_path.name
