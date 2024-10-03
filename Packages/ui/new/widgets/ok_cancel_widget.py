from typing import callable, Union
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QWidget


class OkCancelWidget(QWidget):
    
    
    def __init__(
        self,
        ok_text: str = 'Ok',
        ok_func: Union[callable, None] = None,
        cancel_text: str = 'Cancel',
        cancel_func: Union[callable, None] = None
    ):
        super(OkCancelWidget, self).__init__()
        
        self._ok_method: callable = ok_func
        self._cancel_method: callable = cancel_func
        
        self._ok_button: QPushButton = QPushButton(ok_text)
        self._cancel_button: QPushButton = QPushButton(cancel_text)
        
        self._main_layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(self._main_layout)
        
        self._main_layout.addWidget(self._ok_button)
        self._main_layout.addWidget(self._cancel_button)
        
        self._ok_button.clicked.connect(self._ok_method)
        self._cancel_button.clicked.connect(self._cancel_method)
        