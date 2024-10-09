from typing import Union
from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QTextEdit, QPushButton


class InputDialogMultiLine(QDialog):
    
    
    def __init__(self, parent, title: str, label: str, text: Union[str, None] = None):
        super(InputDialogMultiLine, self).__init__(parent)
        
        self.setWindowTitle(title)
        self.setMaximumSize(200,200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.move(QCursor.pos())
        
        self._label: QLabel = QLabel(label)
        self._text_edit: QTextEdit = QTextEdit(text if text else '')
        self._text_edit.moveCursor(self._text_edit.textCursor().End)
        self._ok_button: QPushButton = QPushButton('Ok')
        self._cancel_button: QPushButton = QPushButton('Cancel')
        
        self._main_layout: QGridLayout = QGridLayout(self)
        
        self._main_layout.addWidget(self._label, 0, 0, 1, 2)
        self._main_layout.addWidget(self._text_edit, 1, 0, 1, 2)
        self._main_layout.addWidget(self._ok_button, 2, 0)
        self._main_layout.addWidget(self._cancel_button, 2, 1)
        
        self._ok_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)
        
        
    @property
    def text(self) -> Union[str, None]:
        return self._text_edit.toPlainText()
