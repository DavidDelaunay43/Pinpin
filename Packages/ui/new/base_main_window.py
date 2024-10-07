from dataclasses import asdict
from functools import partial
from pathlib import Path
from typing import Union
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QButtonGroup, QDesktopWidget, QGridLayout, QHBoxLayout, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from Packages.ui.new import widgets
from Packages.utils.core import Core
from Packages.utils.logger import Logger
from Packages.utils.naming import PipeRoot


class BaseMainWindow(QMainWindow):
    
    
    def __init__(self, project_path: Path, parent: Union[QApplication, None] = None) -> None:
        super(BaseMainWindow, self).__init__(parent)
        
        self._PARENT: QApplication = self.parent()
        self.project_path: Path = project_path
        self.project_name: str = project_path.name
        self.current_path: Path = project_path
        
        self._create_ui()
        self.auto_clic(Core.pref_infos().LAST_PATHS)
    
    
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
        self._tree_widget: widgets.TreeWidget = widgets.TreeWidget()
        self._list_01: widgets.ListWidget = widgets.ListWidget()
        self._list_02: widgets.ListWidget = widgets.ListWidget()
        self._list_03: widgets.ListWidget = widgets.ListWidget()
        self._table_widget: widgets.TableWidget = widgets.TableWidget()

            
            
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
        self._create_browser_grid_layout()
        
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
        self._root_buttons_layout.setContentsMargins(5,5,5,5)
        
        # Add widgets
        for button in self._root_buttons:
            self._root_buttons_layout.addWidget(button)

        self._root_buttons_layout.addStretch(1)
        
        
    def _create_browser_grid_layout(self) -> None:
        
        # Create widget
        self._browser_grid_widget: QWidget = QWidget()
        self._browser_main_layout.addWidget(self._browser_grid_widget)
        
        # Create layout
        self._browser_grid_layout: QGridLayout = QGridLayout()
        self._browser_grid_layout.setContentsMargins(0,0,0,0)
        self._browser_grid_widget.setLayout(self._browser_grid_layout)
        
        # Add widgets
        self._browser_grid_layout.addWidget(self._tree_widget, 0, 0, 3, 1)
        self._browser_grid_layout.addWidget(self._list_01, 0, 1)
        self._browser_grid_layout.addWidget(self._list_02, 0, 2)
        self._browser_grid_layout.addWidget(self._list_03, 0, 3)
        self._browser_grid_layout.addWidget(self._table_widget, 1, 1, 2, 3)
        
        self._browser_grid_layout.setRowStretch(0, 1)
        self._browser_grid_layout.setRowStretch(1, 2)
        self._browser_grid_layout.setRowStretch(2, 2)
        self._browser_grid_layout.setColumnStretch(0, 1)
        self._browser_grid_layout.setColumnStretch(1, 2)
        self._browser_grid_layout.setColumnStretch(2, 2)
        self._browser_grid_layout.setColumnStretch(3, 2)
   
            
    def _create_recent_central_layout(self) -> None:
        
        # Create widget
        self._recent_tab: QWidget = QWidget()
        self._tab_widget.addTab(self._recent_tab, 'Recent')

    
    # ------------------------------------------------------------------------------------------------------
    def _create_connections(self) -> None:
        
        for root_button in self._root_buttons:
            root_button.toggled.connect(self._update_current_path)
            root_button.toggled.connect(
                partial(self._populate_widget, widget=self._tree_widget)
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
        self._list_03.itemClicked.connect(
            partial(self._populate_widget, widget=self._table_widget)
        )
        
        self._table_widget.itemClicked.connect(self._update_current_path)
    
    
    # ------------------------------------------------------------------------------------------------------
    def _update_current_path(self, 
                             item: Union[widgets.PipelineWidgetItem, None] = None, 
                             column: Union[int, None] = None
                             ) -> None:
        
        sender: Union[
            widgets.CheckableButton, widgets.PipelineWidgetItem
        ] = self.sender() if isinstance(self.sender(), widgets.CheckableButton) else item
        
        self.current_path = sender.pipeline_path
        self._status_bar.pipeline_path = sender.pipeline_path
        self.update_memo_path()
        Logger.debug(f'Update current path: {self.current_path}')


    def _populate_widget(self,
                         item: Union[widgets.PipelineWidgetItem, None] = None, 
                         column: Union[int, None] = None, 
                         widget: Union[widgets.PipelineWidget, None] = None
                         ) -> None:
        
        if widget is self._tree_widget:
            self._list_01.populate_update_path(None)
            self._list_02.populate_update_path(None)
            self._list_03.populate_update_path(None)
            self._table_widget.populate_update_path(None)
            widget.populate_update_path(self.current_path)
            return
            
        if widget is self._list_01:
            self._list_02.populate_update_path(None)
            self._list_03.populate_update_path(None)
            self._table_widget.populate_update_path(None)
            widget.populate_update_path(self.current_path)
            return
            
        if widget is self._list_02:
            self._list_03.populate_update_path(None)
            self._table_widget.populate_update_path(None)
            widget.populate_update_path(self.current_path)
            return
        
        widget.populate_update_path(self.current_path)
        

    def update_memo_path(self) -> None:
        
        from Packages.utils.json_file import JsonFile
        
        memo_path_jsonfile: JsonFile = Core.prefs_paths().MEMO_PATH_JSONFILE
        last_paths: list = memo_path_jsonfile.json_to_dict()['last_paths']
        
        Logger.debug(f'{last_paths}')
        
        for index, path in enumerate(last_paths):
            
            if str(self.current_path) == path:
                return
            
            match_path: Path = Core.find_root_dirpath(self.current_path, self.project_path)
            Logger.debug(f'Current path: {self.current_path}\nLast path: {path}')
            if match_path and str(match_path) in path or str(self.current_path) in path:
                last_paths.pop(index)
        
        last_paths.insert(0, str(self.current_path))
        
        memo_path_jsonfile.dict_to_json({"last_paths": last_paths})
        
        
    def _auto_clic_widget(self, widget: widgets.PipelineWidget, next_widget: widgets.PipelineWidget, path: Path) -> None:
        
        column: int = 1 if isinstance(widget, widgets.TreeWidget) else 0
        
        for item in widget.iter_items():
            if path == item.pipeline_path:
                widget.setCurrentItem(item)
                self._update_current_path(item, column)
                self._populate_widget(item, column, next_widget)
                
        
    def auto_clic(self, last_paths: list[str]) -> None:
        
        if not last_paths:
            return
        
        all_paths: list[Path] = [Path(last_paths[0])]
        all_paths.extend(all_paths[0].parents)
        
        for parent in reversed(all_paths):
            
            for root_button in self._root_buttons:
                if parent == root_button.pipeline_path:
                    root_button.setChecked(True)
                    break
                    
            self._auto_clic_widget(self._tree_widget, self._list_01, parent)
            self._auto_clic_widget(self._list_01, self._list_02, parent)
            self._auto_clic_widget(self._list_02, self._list_03, parent)
            self._auto_clic_widget(self._list_03, self._table_widget, parent)
