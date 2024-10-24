from pathlib import Path
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton
from maya import cmds
from Packages.apps.maya_app.ui.maya_line_edit import MayaLineEdit
from Packages.apps.maya_app.utils.maya_file_info import init_file_info
from Packages.apps.maya_app.utils.ui_utils import mayaMainWindow


class IncrementDialog(QDialog):


    def __init__(self, parent):
        super(IncrementDialog, self).__init__(parent)

        self._current_path: Path = Path(cmds.file(query=True, sceneName=True))
        self._file_info = init_file_info(self._current_path)

        self.setWindowTitle('Increment file')

        self._main_layout: QGridLayout = QGridLayout(self)
        self.setLayout(self._main_layout)

        self._current_name_label: QLabel = QLabel(f'Current: {self._current_path.name}')
        self._current_name_label.setStyleSheet("font-size: 16px;")
        self._main_layout.addWidget(self._current_name_label, 0, 0, 1, 2)

        self._save_as_line_edit: MayaLineEdit = MayaLineEdit(self)
        self._save_as_line_edit.setReadOnly(True)
        self._save_as_line_edit.setText(self._file_info.NEXT_PIPELINE_NAME)
        self._save_as_line_edit.setStyleSheet("font-size: 16px; color: rgb(128, 255, 141); font-weight: bold;")
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
        self._file_info.incremental_save(
            path_override=self._current_path.parent.joinpath(
                self._save_as_line_edit.text()
            )
        )
        self.close()


def main() -> None:
    inrement_dialog: IncrementDialog = IncrementDialog(mayaMainWindow())
    inrement_dialog.exec_()
