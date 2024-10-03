from dataclasses import asdict
from pathlib import Path
from typing import Union
from PySide2.QtWidgets import *
from Packages.ui.new import widgets
from Packages.utils.naming import PipeRoot


class BaseMainWindow(QMainWindow):
    
    
    def __init__(self, project_path: Path, parent: Union[QApplication, None] = None) -> None:
        super(BaseMainWindow, self).__init__(parent)
        
        self.project_path: Path = project_path
        self.project_name: str = project_path.name
        self.current_path: Path = None
        
        self.create_ui()
    
    
    # ------------------------------------------------------------------------------------------------------
    def create_ui(self, set_style: bool = False) -> None:
        
        if isinstance(self.parent(), QApplication):
            self._set_style()
        
        self._create_widgets()
        self._create_layout()
        self._create_connections()
        self._create_context_menu()
        
    
    # ------------------------------------------------------------------------------------------------------
    def _create_widgets(self) -> None:
        
        self._menu_bar: widgets.MenuBar = widgets.MenuBar()
        
        self._create_tabs()
        
        self._status_bar: widgets.StatusBar = widgets.StatusBar()
        
        self.root_buttons: list[widgets.CheckableButton] = [self.create_root_button(dirname) for dirname in asdict(PipeRoot).values()]
        
        
    def _create_tabs(self) -> None:
        
        self._tab_widget: QTabWidget = QTabWidget()
        self._browser_tab: QWidget = QWidget()
        self._recent_tab: QWidget = QWidget()

        
    def _create_root_button(self, dirname: str) -> widgets.CheckableButton:
        
        button: widgets.CheckableButton = widgets.CheckableButton(dirname.split('_')[-1].capitalize())
        button.pipeline_path = self.project_path.joinpath(dirname)
        
        return button
    
    # ------------------------------------------------------------------------------------------------------
    def _create_layout(self) -> None:
        
        self._create_root_buttons_layout()
        self._create_browser_main_layout()
        self._create_browser_central_layout()
        
        
        
    def _create_browser_central_layout(self) -> None:
        
        self._central_widget: QWidget = QWidget()
        self.setCentralWidget()
        self._central_layout: QVBoxLayout = QVBoxLayout()
        self._central_widget.setLayout(self._central_layout)
        
        self._central_layout.addWidget(self._tab_widget)
        self._central_layout.addWidget(self._status_bar)
        
    
    def _create_browser_main_layout(self) -> None:
        
        self._browser_main_layout: QVBoxLayout = QVBoxLayout()
        self._browser_main_layout.setContentsMargins(0,0,0,0)
        
        
    def _create_root_buttons_layout(self) -> None:
        
        self._root_buttons_widget: QWidget = QWidget()
        self._root_buttons_layout: QHBoxLayout = QHBoxLayout(self._root_buttons_widget)
        self._root_buttons_layout.setContentsMargins(10,10,10,10)
        
        for button in self.root_buttons:
            self._root_buttons_layout.addWidget(button)

    
    # ------------------------------------------------------------------------------------------------------
    def _create_connections(self) -> None:
        pass
    
    
    # ------------------------------------------------------------------------------------------------------
    def _create_context_menu(self) -> None:
        pass
    
    
    # ------------------------------------------------------------------------------------------------------
    def _set_style(self) -> None:
        pass
