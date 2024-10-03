from pathlib import Path
from typing import Union
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel


class PixmapLabel(QLabel):
    
    
    def __init__(self, icon_path: Union[Path, None] = None) -> None:
        super(PixmapLabel, self).__init__()
        
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        if icon_path:
            self.setPixmap(QPixmap(icon_path))
