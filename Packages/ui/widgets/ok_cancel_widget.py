from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton

class OkCancelWidget(QWidget):

    def __init__(self, parent = None, ok_text = '', ok_func = None, cancel_func = None) -> None:
        super().__init__(parent)

        self._main_layout = QHBoxLayout()
        self.setLayout(self._main_layout)

        self._cancel_button = QPushButton('Cancel')
        self._ok_button = QPushButton(ok_text)

        self._main_layout.addWidget(self._ok_button)
        self._main_layout.addWidget(self._cancel_button)
        
        self._cancel_button.clicked.connect(cancel_func)
        self._ok_button.clicked.connect(ok_func)
