from pathlib import Path
from typing import Union
from maya import cmds
from PySide2.QtWidgets import QCheckBox, QComboBox, QDialog, QFileDialog, QFrame, QLabel, QPushButton
from Packages.apps.maya_app.ui.maya_line_edit import MayaLineEdit
from Packages.apps.maya_app.utils.maya_file_info import init_file_info, MayaShotFileInfo
from Packages.apps.maya_app.utils.ui_utils import mayaMainWindow
from Packages.ui.new.widgets import GridLayout


class CharFrame(QFrame):


    def __init__(self, parent, file_name: str, char_name: str, enabled: bool = True):
        super(CharFrame, self).__init__(parent)

        self._main_layout: GridLayout = GridLayout(self)
        self._main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self._main_layout)

        self.check_box: QCheckBox = QCheckBox(char_name.upper(), self)
        self.check_box.setChecked(enabled)
        self.check_box.clicked.connect(self._toggle_file_name_line_edit)
        self._main_layout.addWidget(self.check_box, 0, 0)

        self.file_name_line_edit: MayaLineEdit = MayaLineEdit(self)
        self.file_name_line_edit.setReadOnly(True)
        self.file_name_line_edit.setText(file_name)
        self.file_name_line_edit.setStyleSheet("font-size: 16px; color: rgb(255, 200, 50);")
        self._main_layout.addWidget(self.file_name_line_edit, 0, 1)


    def _toggle_file_name_line_edit(self) -> None:

        if self.check_box.isChecked():
            self.file_name_line_edit.setEnabled(True)
            self.file_name_line_edit.setStyleSheet("font-size: 16px; color: rgb(255, 200, 50);")
            return
        
        else:
            self.file_name_line_edit.setEnabled(False)
            self.file_name_line_edit.setStyleSheet("font-size: 16px; color: rgb(100, 100, 10);")


class AlembicDialog(QDialog):


    def __init__(self, parent) -> None:
        super(AlembicDialog, self).__init__(parent)

        self.setWindowTitle('Alembic')
        self.setMinimumWidth(800)
        self._char_frames: list[CharFrame] = []
        self._file_info: MayaShotFileInfo = init_file_info(Path(cmds.file(query=True, sceneName=True)))

        self._main_layout: GridLayout = GridLayout(self)
        self.setLayout(self._main_layout)

        self._mode_label: QLabel = QLabel('Select mode:', self)
        self._main_layout.addWidget(self._mode_label, 0, 0, 1, 1)
        
        self._mode_combo_box: QComboBox = QComboBox(self)
        self._mode_combo_box.addItems(['EXPORT', 'IMPORT'])
        self._mode_combo_box.currentIndexChanged.connect(self._toggle_widget_text)
        self._main_layout.addWidget(self._mode_combo_box, 0, 1, 1, 7)

        self._path_label: QLabel = QLabel('Output path:')
        self._main_layout.addWidget(self._path_label, 1, 0, 1, 1)

        self._output_path_line_edit: MayaLineEdit = MayaLineEdit(self)
        self._output_path_line_edit.setText(str(self._file_info.cache_path))
        self._output_path_line_edit.setReadOnly(True)
        self._output_path_line_edit.setStyleSheet("font-size: 16px; color: rgb(120, 200, 255);")
        self._main_layout.addWidget(self._output_path_line_edit, 1, 1, 1, 1)

        self._output_path_browse_button: QPushButton = QPushButton('Browse', self)
        self._output_path_browse_button.clicked.connect(self._get_path)
        self._main_layout.addWidget(self._output_path_browse_button, 1, 2, 1, 6)

        self._populate_char_frame([
            'roger',
            'marcel',
            'riton',
            'hilaire'
        ])

        self._run_button: QPushButton = QPushButton('EXPORT ALEMBICS', self)
        self._run_button.setMinimumHeight(50)
        self._main_layout.addWidget(self._run_button, self._main_layout.first_empty_row(), 0, 1, 8)


    @property
    def project_prefix(self) -> str:
        return self._file_info.project_prefix
    

    @property
    def sequence_num(self) -> Union[str, None]:
        return self._file_info.sequence_num
    

    @property
    def shot_num(self) -> Union[str, None]:
        return self._file_info.shot_num
    

    @property
    def department(self) -> Union[str, None]:
        return self._file_info.department
    

    def export_abc(self) -> None:
        pass


    def import_abc(self) -> None:
        pass
    

    def _populate_char_frame(self, char_names: list[str] = None) -> None:
        if not char_names:
            return

        for char_name in char_names:
            self._add_char_frame(char_name)


    def _add_char_frame(self, char_name: str) -> None:

        file_name: str = '_'.join(
            [
                self.project_prefix,
                self.sequence_num,
                self.shot_num,
                char_name,
                self.department
            ]
        ) + '.abc'

        char_frame: CharFrame = CharFrame(self, file_name, char_name)
        self._main_layout.addWidget(char_frame, self._main_layout.first_empty_row(), 0, 1, 8)
        self._char_frames.append(char_frame)


    def _toggle_widget_text(self) -> None:
        toggle_dict: dict = {
            0: ('Output path:', 'EXPORT ALEMBICS'),
            1: ('Alembics path:', 'IMPORT ALEMBICS')
        }
        self._path_label.setText(toggle_dict.get(self._mode_combo_box.currentIndex())[0])
        self._run_button.setText(toggle_dict.get(self._mode_combo_box.currentIndex())[1])


    def _get_path(self) -> None:
        
        file_dialog: QFileDialog = QFileDialog(self)
        #file_dialog.setDirectory()
        path: Union[str, None] = file_dialog.getExistingDirectory(self, 'Select alembic path', options = QFileDialog.Options())

        if not path:
            return
        
        self._output_path_line_edit.setText(path)


    def accept(self) -> None:
        self.close()


def main() -> None:
    alembic_dialog: AlembicDialog = AlembicDialog(mayaMainWindow())
    alembic_dialog.exec()
