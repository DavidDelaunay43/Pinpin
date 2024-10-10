from pathlib import Path
from typing import Union
from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QColor, QFont, QIcon
from PySide2.QtWidgets import QTableWidgetItem


class TableWidgetItem(QTableWidgetItem):
    
    
    def __init__(self, path: Path, text: str = '', icon: Union[Path, None] = None, size: Union[int, None] = None):
        super(TableWidgetItem, self).__init__()
    
        self._pipeline_path: Path = path
        
        self.setToolTip(
            f'<span style="font-size: 14px; background-color: white; color: black; border: 0px transparent;">{self.pipeline_name}</span>'
        )
        
        if icon:
            self.setIcon(QIcon(str(icon)))
            return
        
        if text:
            self.setText(text)
            self.setTextAlignment(Qt.AlignCenter)
            if size:
                self.setFont(QFont(QFont().family(), size))
                
            color_dict = {
                '.hip': [255, 150, 150],
                '.hipnc': [255, 150, 150],
                '.ma': [150, 255, 255],
                '.mb': [150, 255, 255],
                '.nk': [255, 200, 150],
                '.nknc': [255, 200, 150]
            }
            for ext in color_dict.keys():
                if ext in text:
                    self.setForeground(QBrush(QColor(*color_dict[ext])))
                    break
              
    
    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path) -> None:
        self._pipeline_path = path
    
    
    @property
    def pipeline_name(self) -> str:
        return self._pipeline_path.name if self._pipeline_path else None
