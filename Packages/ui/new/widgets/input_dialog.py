from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QInputDialog


class InputDialog(QInputDialog):
    
    
    def __init__(self, parent, title: str, label: str):
        super(InputDialog, self).__init__(parent)
        
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.move(QCursor.pos())
        self.setStyle(None)
