from functools import partial
from pathlib import Path
from typing import Literal, Union
from PySide2.QtCore import Qt, QPoint, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAction, QFileDialog, QHBoxLayout, QMenu, QPushButton, QWidget
from Packages.utils.core import Core
from Packages.utils.file_opener import FileOpener
from Packages.utils.json_file import JsonFile
from Packages.utils.logger import Logger


class OpenFileWidget(QWidget):
    
    
    def __init__(self, path: Union[Path, None] = None, dev_mode: bool = False, ui_pref_jsonfile: Union[JsonFile, None] = None) -> None:
        super(OpenFileWidget, self).__init__()
        
        self._pipeline_path: Union[Path, None] = path
        self._dev: bool = dev_mode
        self._ui_pref_jsonfile: Union[JsonFile, None] = ui_pref_jsonfile
        self._file_opener: FileOpener = FileOpener(path)
        
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
    
    
    def update_widget(self, path: Union[Path, None]) -> None:
        self.pipeline_path = path
        if not path:
            self.open_button.setText('Open file in')
            self.prefs_button.setText('')
            self.python_button.setText('')
            return
        
        self._file_opener.update_infos(path)
        self.open_button.setText(f'Open file in {self._file_opener.software_name.capitalize() if self._file_opener.software_name else ""}')
        self.prefs_button.setText(f'{self._file_opener.pref_path.name if self._file_opener.pref_path else ""}')
        self.python_button.setText(f'{self._file_opener.python_path.name if self._file_opener.python_path else ""}')
    
    
    def _create_connections(self) -> None:
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
        self.open_button.clicked.connect(self.open_file)
        self.prefs_button.clicked.connect(self._set_pref_path)
        self.python_button.clicked.connect(self._set_python_path)
    
    
    def _create_context_menu(self) -> None:
        
        self._context_menu: QMenu = QMenu()
        
        self._dev_button_action: QAction = QAction('Show/Hide Dev buttons')
        self._reset_pref_action: QAction = QAction('Reset prefs path')
        self._reset_python_action: QAction = QAction('Reset Python path')
        
        self._dev_button_action.triggered.connect(self._toggle_dev_buttons)
        self._reset_pref_action.triggered.connect(partial(self._set_pref_path, reset=True))
        self._reset_python_action.triggered.connect(partial(self._set_python_path, reset=True))
        
        self._context_menu.addAction(self._dev_button_action)
        self._context_menu.addSeparator()
        self._context_menu.addAction(self._reset_pref_action)
        self._context_menu.addAction(self._reset_python_action)
        
    
    def _show_context_menu(self, pos: QPoint):
        self._context_menu.exec_(self.mapToGlobal(pos))
    
    
    def _toggle_dev_buttons(self) -> None:
        
        self.prefs_button.setVisible(not self._dev)
        self.python_button.setVisible(not self._dev)
        self._dev = not self._dev
        self._ui_pref_jsonfile.set_value('dev_mode', self._dev)
        
        
    def open_file(self) -> None:
        self._file_opener.open_file()
        
        
    def _set_pref_path(self, reset: bool = False) -> None:
        self._set_path('pref', reset=reset)
    
    
    def _set_python_path(self, reset: bool = False) -> None:
        self._set_path('python_path', reset=reset)
        
        
    def _set_path(self, path_type: Literal['pref', 'python_path'], reset: bool = False) -> Union[Path, None]:
        
        all_apps_dict: dict = Core.prefs_paths().APPS_JSONFILE.json_to_dict()
        app_name: str = self._file_opener.software_name
            
        if not reset:
            file_dialog: QFileDialog = QFileDialog()
            file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
            file_dialog.setDirectory(str(Path.home()))
            path = file_dialog.getExistingDirectory(self, 'Select directory', options = QFileDialog.Options())
            
            if not path:
                return
            
            path = Path(path)
            
            if not app_name in all_apps_dict.keys():
                return
            
            all_apps_dict[app_name][path_type] = str(path)
            
        else:
            path = None
            all_apps_dict[app_name][path_type] = None
        
        Core.prefs_paths().APPS_JSONFILE.dict_to_json(all_apps_dict)
        Logger.info(f'Update {app_name} {path_type}: {path}')
        
        self.update_widget(self.pipeline_path)
        self._file_opener.update_infos(self.pipeline_path)

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