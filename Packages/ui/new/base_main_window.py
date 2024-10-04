from dataclasses import asdict
from functools import partial
from pathlib import Path
from typing import Union
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QButtonGroup, QDesktopWidget, QHBoxLayout, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from Packages.ui.new import widgets
from Packages.utils.core import Core
from Packages.utils.naming import PipeRoot


class BaseMainWindow(QMainWindow):
    
    
    def __init__(self, project_path: Path, parent: Union[QApplication, None] = None) -> None:
        super(BaseMainWindow, self).__init__(parent)
        
        self._PARENT: QApplication = self.parent()
        self.project_path: Path = project_path
        self.project_name: str = project_path.name
        self.current_path: Path = project_path
        
        self._create_ui()
    
    
    # ------------------------------------------------------------------------------------------------------
    def _create_ui(self) -> None:
        
        self._init_ui()
        self._create_widgets()
        self._create_layout()
        self._create_connections()
        self.setMenuBar(widgets.MenuBar())
        
        self._status_bar.pipeline_path = self.current_path
        
        
    def _init_ui(self) -> None:
        
        self.resize(820, 900)
        self._move_main_window()
            
        self.setWindowTitle(f'Pinpin - {Core.current_version()} - {Core.current_project_path().name}')
        self.setWindowIcon(QIcon(str(Core.pinpin_icon_path())))
        
        if isinstance(self._PARENT, QApplication):
            self._set_style()
        
        
    def _move_main_window(self) -> None:
        
        if self._PARENT:
            parent_geo = self._PARENT.geometry()
            self.move(
                parent_geo.x()+(parent_geo.width()-self.width())//2,
                parent_geo.y()+(parent_geo.height()-self.height())//2+40
            )
            return
        
        desktop: QDesktopWidget = QDesktopWidget()
        self.move(
            (desktop.screen().width()-self.width())//2,
            (desktop.screen().height()-self.height())//2-40
        )
        
    
    def _set_style(self) -> None:
        pass
    
        
    # ------------------------------------------------------------------------------------------------------
    def _create_widgets(self) -> None:
        
        self._tab_widget: QTabWidget = QTabWidget()
        self._status_bar: widgets.StatusBar = widgets.StatusBar()
        self._create_root_buttons()
        self._tree_widget: widgets.TreeWidget = widgets.TreeWidget(self.current_path)
        self._list_01: widgets.ListWidget = widgets.ListWidget(self.current_path)
        self._list_02: widgets.ListWidget = widgets.ListWidget(self.current_path)
        self._list_03: widgets.ListWidget = widgets.ListWidget(self.current_path)
            
            
    def _create_root_buttons(self) -> None:

        self._root_button_group: QButtonGroup = QButtonGroup()
        
        self._root_buttons: list[widgets.CheckableButton] = [
            widgets.CheckableButton(
                path = self.current_path.joinpath(dirname),
                text = dirname.split('_')[-1].capitalize()
            )
            for dirname in asdict(PipeRoot()).values()
        ]
        
        for root_button in self._root_buttons:
            self._root_button_group.addButton(root_button)


    # ------------------------------------------------------------------------------------------------------
    def _create_layout(self) -> None:
        
        self._create_central_layout()
        
        self._create_browser_main_layout()
        self._create_root_buttons_layout()
        self._create_browser_hlayout()
        self._create_browser_vlayout()
        self._create_browser_lists_layout()
        
        self._create_recent_central_layout()
        
        
    def _create_central_layout(self) -> None:
        
        # Create widget
        self._central_widget: QWidget = QWidget()
        self.setCentralWidget(self._central_widget)
        
        # Create layout
        self._central_layout: QVBoxLayout = QVBoxLayout()
        self._central_widget.setLayout(self._central_layout)
        
        # Add widgets
        self._central_layout.addWidget(self._tab_widget)
        self._central_layout.addWidget(self._status_bar)
        
        
    def _create_browser_main_layout(self) -> None:
        
        # Create widget
        self._browser_tab: QWidget = QWidget()
        self._tab_widget.addTab(self._browser_tab, 'Browser')
        
        # Create layout
        self._browser_main_layout: QVBoxLayout = QVBoxLayout()
        self._browser_main_layout.setContentsMargins(0,0,0,0)
        self._browser_tab.setLayout(self._browser_main_layout)
        
        
    def _create_root_buttons_layout(self) -> None:
        
        # Create widget
        self._root_buttons_widget: QWidget = QWidget()
        self._browser_main_layout.addWidget(self._root_buttons_widget)
        
        # Create layout
        self._root_buttons_layout: QHBoxLayout = QHBoxLayout(self._root_buttons_widget)
        self._root_buttons_layout.setContentsMargins(10,10,10,10)
        
        # Add widgets
        for button in self._root_buttons:
            self._root_buttons_layout.addWidget(button)

        self._root_buttons_layout.addStretch(1)
            
            
    def _create_browser_hlayout(self) -> None:
        
        # Create widget
        self._browser_hwidget: QWidget = QWidget()
        self._browser_main_layout.addWidget(self._browser_hwidget)
        
        # Create layout
        self._browser_hlayout: QHBoxLayout = QHBoxLayout()
        self._browser_hwidget.setLayout(self._browser_hlayout)
        
        # Add widgets
        self._browser_hlayout.addWidget(self._tree_widget)
        self._browser_hlayout.addStretch(1)
        
        
    def _create_browser_vlayout(self) -> None:
        
        # Create widget
        self._browser_vwidget: QWidget = QWidget()
        self._browser_hlayout.addWidget(self._browser_vwidget)
        
        # Create layout
        self._browser_vlayout: QVBoxLayout = QVBoxLayout()
        self._browser_vwidget.setLayout(self._browser_vlayout)
        
        # Add widgets
        
    
    def _create_browser_lists_layout(self) -> None:
        
        # Create widget
        self._browser_list_widget: QWidget = QWidget()
        self._browser_vlayout.addWidget(self._browser_list_widget)
        
        # Create layout
        self._browser_list_layout: QHBoxLayout = QHBoxLayout()
        self._browser_list_widget.setLayout(self._browser_list_layout)
        
        # Add widgets
        self._browser_list_layout.setAlignment(Qt.AlignTop) 
        self._browser_list_layout.addWidget(self._list_01)
        self._browser_list_layout.addWidget(self._list_02)
        self._browser_list_layout.addWidget(self._list_03)
        
            
    def _create_recent_central_layout(self) -> None:
        
        # Create widget
        self._recent_tab: QWidget = QWidget()
        self._tab_widget.addTab(self._recent_tab, 'Recent')

    
    # ------------------------------------------------------------------------------------------------------
    def _create_connections(self) -> None:
        
        for root_button in self._root_buttons:
            root_button.clicked.connect(self._update_current_path)
            root_button.clicked.connect(
                partial(self._tree_widget.populate, self.current_path.joinpath(root_button.pipeline_name))
            )
            
        self._tree_widget.itemClicked.connect(self._update_current_path)
        self._tree_widget.itemClicked.connect(
            partial(self._populate_widget, widget=self._list_01)
        )
        
        self._list_01.itemClicked.connect(self._update_current_path)
        self._list_01.itemClicked.connect(
            partial(self._populate_widget, widget=self._list_02)
        )
        
        self._list_02.itemClicked.connect(self._update_current_path)
        self._list_02.itemClicked.connect(
            partial(self._populate_widget, widget=self._list_03)
        )
        
        self._list_03.itemClicked.connect(self._update_current_path)
    
    
    # ------------------------------------------------------------------------------------------------------
    def _update_current_path(self, item: widgets.TreeWidgetItem = None, column: int = None) -> None:
        
        sender: Union[
            widgets.CheckableButton, widgets.TreeWidgetItem
        ] = self.sender() if isinstance(self.sender(), widgets.CheckableButton) else item
        
        self.current_path = sender.pipeline_path
        self._status_bar.pipeline_path = sender.pipeline_path


    def _populate_widget(self, item: widgets.TreeWidgetItem = None, column: int = None, widget = None) -> None:
        
        sender: Union[
            widgets.CheckableButton, widgets.TreeWidgetItem
        ] = self.sender() if isinstance(self.sender(), widgets.CheckableButton) else item
        
        self.current_path = sender.pipeline_path
        widget.populate(self.current_path)
