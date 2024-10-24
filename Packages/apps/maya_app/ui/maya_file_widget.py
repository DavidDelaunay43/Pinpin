from functools import partial
from pathlib import Path
from typing import Union
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QComboBox, QGridLayout, QLineEdit, QPushButton, QWidget
from Packages.apps.maya_app.utils.enums import GetMode, Get, Namespace
from Packages.apps.maya_app.utils.maya_file_getter import MayaFileGetter
from Packages.utils.core import Core
from Packages.utils.logger import Logger


class MayaFileWidget(QWidget):


    def __init__(self, parent = None, pipeline_path: Union[Path, None] = None):
        super(MayaFileWidget, self).__init__(parent)

        self._pipeline_path: Path = pipeline_path
        self._mode: GetMode = GetMode.OPEN
        self._getter: MayaFileGetter = MayaFileGetter(pipeline_path, GetMode.OPEN)

        self._init_ui()


    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    

    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
        self._getter.pipeline_path = path


    def _init_ui(self):
        
        self._main_layout: QGridLayout = QGridLayout(self)
        self.setLayout(self._main_layout)

        self._get_file_combo_box: QComboBox = QComboBox(self)
        self._get_file_combo_box.addItems([mode.value for mode in Get])
        self._main_layout.addWidget(self._get_file_combo_box, 0, 0, 1, 1)

        self._namespace_comobo_box: QComboBox = QComboBox(self)
        self._namespace_comobo_box.addItems([namespace.value for namespace in Namespace])
        self._main_layout.addWidget(self._namespace_comobo_box, 0, 1, 1, 1)
        
        self._namespace_line_edit: QLineEdit = QLineEdit(self)
        self._main_layout.addWidget(self._namespace_line_edit, 1, 0, 1, 2)

        self._file_button: QPushButton = QPushButton(self)
        self._file_button.setMinimumHeight(50)
        self._main_layout.addWidget(self._file_button, 0, 2, 2, 3)

        self._update_mode()
        self._create_connections()


    def _create_connections(self) -> None:
        self._get_file_combo_box.currentIndexChanged.connect(self._update_mode)
        self._namespace_comobo_box.currentIndexChanged.connect(self._update_mode)
        self._file_button.clicked.connect(self._get_file)


    def _get_file(self) -> None:
        self._getter.custom_namespace = self._namespace_line_edit.text()
        self._getter.get_file()


    def _update_mode(self) -> None:
        self._file_button.setIcon(
            QIcon(
                str(Core.pinpin_icons_path().joinpath(f'{self._get_file_combo_box.currentText().lower()}_icon.ico'))
            )
        )

        get_mode_text: str = self._get_file_combo_box.currentText()
        namespace_text: str = self._namespace_comobo_box.currentText()
        string_mode: str = ''

        string_mode = get_mode_text if get_mode_text=='Open' else f'{get_mode_text} {namespace_text}'
        self._namespace_comobo_box.setEnabled(False if get_mode_text=='Open' else True)

        self._file_button.setText(string_mode)
        self._mode = [mode for mode in GetMode if mode.value == string_mode][0]
        self._getter.mode = self._mode

        Logger.debug(f'Update mode: {string_mode}')


    def update_widget(self, path: Path) -> None:
        if path and not path.exists():
            Logger.error(f'{path} does not exists.')
            return
        
        self.pipeline_path = path
