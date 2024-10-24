from pathlib import Path
from typing import Union
from PySide2.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget
from Packages.utils.core import Core


class SettingsWidget(QWidget):


    def __init__(self, path: Union[Path, None] = None) -> None:
        super(SettingsWidget, self).__init__()

        self.project_path: Union[Path, None] = path

        self._create_widgets()
        self._create_layout()
        self._create_connections()


    def _create_widgets(self) -> None:
        
        self.project_button: QPushButton = QPushButton(self.project_path.name)
        self.project_path_label: QLabel = QLabel(str(self.project_path))

        self._info_label: QLabel = QLabel(Core.info_html_path().read_text(encoding='utf-8'))
        self._info_label.setWordWrap(True)


    def _create_layout(self) -> None:
        
        self._main_layout: QGridLayout = QGridLayout()
        self.setLayout(self._main_layout)
        self._main_layout.setContentsMargins(20,20,20,20)

        self._main_layout.addWidget(self.project_button, 0, 0)
        self._main_layout.addWidget(self.project_path_label, 1, 0)

        self._main_layout.addWidget(self._info_label, 0, 1, 2, 1)


    def _create_connections(self) -> None:
        pass
