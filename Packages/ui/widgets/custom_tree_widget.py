from PySide2.QtWidgets import QTreeWidget
from PySide2.QtCore import Qt, QSize

class CustomTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumWidth(250)
        self.setHeaderHidden(True)
        self.setTextElideMode(Qt.ElideNone)
        self.setAnimated(True)
        self.header().setVisible(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("font-size: 14px;")
        self.setIconSize(QSize(35, 35))

    """def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            if index.isValid():
                self.setExpanded(index, not self.isExpanded(index))  # Expand or collapse the item
        super().mousePressEvent(event)"""
        