import os
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel
from Packages.utils.constants import ICON_PATH

ALIGNMENT_DICT = {
    'center': Qt.AlignmentFlag.AlignCenter,
    'left': Qt.AlignmentFlag.AlignLeft,
    'right': Qt.AlignmentFlag.AlignRight
}

class CustomLabel(QLabel):
    
    def __init__(self, text = '', parent = None, alignment = 'left'):
        super(CustomLabel, self).__init__(text)
        
        self.setAlignment(ALIGNMENT_DICT[alignment])
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        if parent:
            parent.addWidget(self)
            
    def add_pixmap(self, icon_filename: str, pixmap_size = None):
        """
        """
        
        icon_filepath = os.path.join(ICON_PATH, icon_filename)
        pixmap = QPixmap(icon_filepath)
        
        if pixmap_size:
            pixmap = pixmap.scaled(*pixmap_size, Qt.KeepAspectRatio)
        
        self.setPixmap(pixmap)
