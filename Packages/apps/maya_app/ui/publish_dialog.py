from pathlib import Path
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from maya import cmds
from Packages.apps.maya_app.ui.maya_line_edit import MayaLineEdit
from Packages.apps.maya_app.utils.maya_file_info import init_file_info
from Packages.apps.maya_app.utils.ui_utils import mayaMainWindow


class PublishDialog(QDialog):


    def __init__(self, parent):
        super(PublishDialog, self).__init__(parent)

        self._current_path: Path = Path(cmds.file(query=True, sceneName=True))
        self._file_info = init_file_info(self._current_path)

        self.setWindowTitle('Publish file')

        self._main_layout: QGridLayout = QGridLayout(self)
        self.setLayout(self._main_layout)

        self._current_name_label: QLabel = QLabel(f'Current: {self._current_path.name}')
        self._current_name_label.setStyleSheet("font-size: 16px;")
        self._main_layout.addWidget(self._current_name_label, 0, 0, 1, 2)

        self._save_as_line_edit: MayaLineEdit = MayaLineEdit(self)
        self._save_as_line_edit.setReadOnly(True)
        self._save_as_line_edit.setText(self._file_info.publish_file_name)
        self._save_as_line_edit.setStyleSheet("font-size: 16px; color: rgb(128, 192, 255); font-weight: bold;")
        self._main_layout.addWidget(self._save_as_line_edit, 1, 0, 1, 2)

        self._ok_button: QPushButton = QPushButton('Ok', self)
        self._ok_button.clicked.connect(self.accept)
        self._ok_button.setDefault(True)
        self._ok_button.setStyleSheet("font-size: 16px;")
        self._main_layout.addWidget(self._ok_button, 2, 0, 1, 1)

        self._cancel_button: QPushButton = QPushButton('Cancel', self)
        self._cancel_button.clicked.connect(self.reject)
        self._cancel_button.setStyleSheet("font-size: 16px;")
        self._main_layout.addWidget(self._cancel_button, 2, 1, 1, 1)


    def accept(self) -> None:
        self._file_info.publish_file()
        self.close()


def main() -> None:
    inrement_dialog: PublishDialog = PublishDialog(mayaMainWindow())
    inrement_dialog.exec_()
