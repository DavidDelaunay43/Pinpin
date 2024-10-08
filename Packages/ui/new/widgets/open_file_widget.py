from pathlib import Path
from typing import Union
from PySide2.QtCore import Qt, QPoint, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAction, QHBoxLayout, QMenu, QPushButton, QWidget
from Packages.utils.core import Core
from Packages.utils.json_file import JsonFile


class OpenFileWidget(QWidget):
    
    
    def __init__(self, path: Union[Path, None] = None, dev_mode: bool = False, ui_pref_jsonfile: Union[JsonFile, None] = None) -> None:
        super(OpenFileWidget, self).__init__()
        
        self._pipeline_path: Union[Path, None] = path
        self._dev: bool = dev_mode
        self._ui_pref_jsonfile: Union[JsonFile, None] = ui_pref_jsonfile
        
        self._main_layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(self._main_layout)
        self._main_layout.setContentsMargins(0,0,0,0)
        
        self.prefs_button: QPushButton = QPushButton()
        self.open_button: QPushButton = QPushButton('Open file in ')
        self.python_button: QPushButton = QPushButton()
        
        self._main_layout.addWidget(self.prefs_button)
        self._main_layout.addWidget(self.open_button)
        self._main_layout.addWidget(self.python_button)
        
        self.prefs_button.setMinimumHeight(50)
        self.open_button.setMinimumHeight(50)
        self.python_button.setMinimumHeight(50)
        
        self.prefs_button.setIcon(QIcon(str(Core.icon_path('folder_icon.png'))))
        self.prefs_button.setIconSize(QSize(35,35))
        self.python_button.setIcon(QIcon(str(Core.icon_path('python_icon.png'))))
        self.python_button.setIconSize(QSize(35,35))
        self.prefs_button.setMaximumWidth(150)
        self.python_button.setMaximumWidth(150)
        self.prefs_button.setVisible(dev_mode)
        self.python_button.setVisible(dev_mode)
        
        self._create_context_menu()
        self._create_connections()
        
        
    @property
    def pipeline_path(self) -> Union[Path, None]:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Union[Path, None]) -> None:
        self._pipeline_path = path
        
        
    @property
    def pipeline_name(self) -> Union[str, None]:
        return self._pipeline_path.name if self._pipeline_path else None
    
    
    def _create_connections(self) -> None:
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
    
    def _create_context_menu(self) -> None:
        
        self._context_menu: QMenu = QMenu()
        self._dev_button_action: QAction = QAction('Show/Hide Dev buttons')
        self._dev_button_action.triggered.connect(self._toggle_dev_buttons)
        self._context_menu.addAction(self._dev_button_action)
        
        
    def _show_context_menu(self, pos: QPoint):
        self._context_menu.exec_(self.mapToGlobal(pos))
    
    
    def _toggle_dev_buttons(self) -> None:
        
        self.prefs_button.setVisible(not self._dev)
        self.python_button.setVisible(not self._dev)
        self._dev = not self._dev
        self._ui_pref_jsonfile.set_value('dev_mode', self._dev)
        
        
    def _get_prefs_path(self) -> None:
        ...
        
        
    def _open_file(self) -> None:
        ...
        
        
    def _get_python_path(self) -> None:
        ...


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication, QVBoxLayout, QMainWindow
    
    app: QApplication = QApplication([])
    window: QMainWindow = QMainWindow()
    window.setWindowTitle('Open File Widget Example')
    open_file_widget = OpenFileWidget()
    main_layout: QVBoxLayout = QVBoxLayout()
    main_layout.addWidget(open_file_widget)
    central_widget: QWidget = QWidget()
    central_widget.setLayout(main_layout)
    window.setCentralWidget(central_widget)
    window.show()
    app.exec_()