import os
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QWidget
from Packages.utils.core import Core


class CornerWidget(QWidget):
    
    
    def __init__(self, parent = None, text: str = ''):
        super(CornerWidget, self).__init__(parent)
        
        self.setMinimumWidth(50)
        self._main_layout = QHBoxLayout()
        self.setLayout(self._main_layout)
        self._main_layout.setContentsMargins(0,5,10,0)

        self.button: QPushButton = QPushButton(text, self)
        font: QFont = QFont()
        font.setPointSize(10)
        self.button.setFont(font)
        self.button.setIcon(QIcon(str(Core.user_icon())))
        self._main_layout.addWidget(self.button)


    @property
    def username(self) -> str:
        return self.button.text()
    

    @username.setter
    def username(self, text: str) -> None:
        self.button.setText(text)
