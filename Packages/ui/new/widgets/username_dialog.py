import os
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QRadioButton
from Packages.utils.core import Core
from Packages.utils.logger import Logger


class UsernameDialog(QDialog):


    def __init__(self, parent):
        super(UsernameDialog, self).__init__(parent)

        self.setWindowTitle('Username update')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._main_layout: QGridLayout = QGridLayout(self)
        self.setLayout(self._main_layout)

        self._default_user_button: QRadioButton = QRadioButton('Default username:', self)
        self._custom_user_button: QRadioButton = QRadioButton('Override username:', self)
        self._custom_user_button.clicked.connect(self._set_focus_line_edit)
        self._default_user_label: QLabel = QLabel(os.getenv('USERNAME'), self)
        self._custom_user_line_edit: QLineEdit = QLineEdit(self)
        self._ok_button: QPushButton = QPushButton('OK', self)
        self._ok_button.setDefault(True)
        self._ok_button.clicked.connect(self.accept)
        self._cancel_button: QPushButton = QPushButton('Cancel', self)
        self._cancel_button.clicked.connect(self.close)

        self._main_layout.addWidget(self._default_user_button, 0, 0, 1, 1)
        self._main_layout.addWidget(self._default_user_label, 0, 1, 1, 1)
        self._main_layout.addWidget(self._custom_user_button, 1, 0, 1, 1)
        self._main_layout.addWidget(self._custom_user_line_edit, 1, 1, 1, 1)
        self._main_layout.addWidget(self._ok_button, 2, 0, 2, 1)
        self._main_layout.addWidget(self._cancel_button, 2, 1, 2, 1)

        if Core.username() == os.getenv('USERNAME'):
            self._default_user_button.setChecked(True)
        else:
            self._custom_user_button.setChecked(True)
            self._custom_user_line_edit.setText(Core.username())


    def _set_focus_line_edit(self) -> None:
        self._custom_user_line_edit.setFocus()


    def accept(self) -> str:
        Core.set_username(self.USERNAME)
        Logger.info(f'Set username: {self.USERNAME}')
        self.close()

    
    @property
    def USERNAME(self) -> str:
        custom_username: str = self._custom_user_line_edit.text()
        default_username: str = self._default_user_label.text()

        if self._custom_user_button.isChecked():
            return custom_username if custom_username else default_username
        else:
            return default_username
