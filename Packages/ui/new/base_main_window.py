from dataclasses import asdict
from functools import partial
from pathlib import Path
import shutil
from typing import Union
from PySide2.QtCore import QDir
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QButtonGroup, QDesktopWidget, QFileDialog, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QTabWidget, QVBoxLayout, QWidget
from Packages.ui.new import widgets
from Packages.utils.core import Core
from Packages.utils.json_file import JsonFile
from Packages.utils.logger import Logger
from Packages.utils.naming import PipeRoot


class BaseMainWindow(QMainWindow):
    
    
    def __init__(self, project_path: Path, parent: Union[QApplication, None] = None) -> None:
        super(BaseMainWindow, self).__init__(parent)
        
        self._project_path: Path = project_path
        self.current_path: Path = project_path
        
        self._create_ui()
        self.auto_clic(Core.pref_infos().LAST_PATHS)


    @property
    def project_path(self) -> Path:
        return self._project_path
    

    @project_path.setter
    def project_path(self, path: Path) -> None:
        self._project_path = path
    

    @property
    def project_name(self) -> str:
        return self._project_path.name
    
    
    # ------------------------------------------------------------------------------------------------------
    def _create_ui(self) -> None:
        
        self._init_ui()
        self._create_widgets()
        self._create_layout()
        self._create_connections()
        self._status_bar.pipeline_path = self.current_path
        
        
    def _init_ui(self) -> None:
        
        self.resize(850, 950)
        self._move_main_window()
            
        self.setWindowTitle(f'Pinpin | {Core.current_version()} | {Core.current_project_path().name}')
        self.setWindowIcon(QIcon(str(Core.pinpin_icon_path())))
        if not self.parent():
            self._set_style()
        
        
    def _move_main_window(self) -> None:
        
        if self.parent():
            parent_geo = self.parent().geometry()
            self.move(
                parent_geo.x()+(parent_geo.width()-self.width())//2,
                parent_geo.y()+(parent_geo.height()-self.height())//2-40
            )
            return
        
        desktop: QDesktopWidget = QDesktopWidget()
        self.move(
            (desktop.screen().width()-self.width())//2,
            (desktop.screen().height()-self.height())//2-40
        )
        
    
    def _set_style(self) -> None:
        
        QDir.setSearchPaths('icons', [str(Core.style_icons_path())])
        self.setStyleSheet(Core.style_sheet('prism.qss'))
    
        
    # ------------------------------------------------------------------------------------------------------
    def _create_widgets(self) -> None:
        
        self.menu_bar: widgets.MenuBar = widgets.MenuBar()
        self.setMenuBar(self.menu_bar)
        
        self._tab_widget: QTabWidget = QTabWidget(self)
        self._status_bar: widgets.StatusBar = widgets.StatusBar(self)
        self._status_bar_button: QPushButton = QPushButton('Copy path', self)

        self._create_root_buttons()
        self._file_label: widgets.FileLabel = widgets.FileLabel(self)
        self._file_label.setVisible(False)
        self._tree_widget: widgets.TreeWidget = widgets.TreeWidget()
        self._list_01: widgets.ListWidget = widgets.ListWidget()
        self._list_02: widgets.ListWidget = widgets.ListWidget()
        self._list_03: widgets.ListWidget = widgets.ListWidget()
        self._table_widget: widgets.TableWidget = widgets.TableWidget(self)

        self._settings_widget: widgets.SettingsWidget = widgets.SettingsWidget(path=self._project_path)

    
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
        
        self._create_settings_central_layout()

        
    def _create_central_layout(self) -> None:
        
        # Create widget
        self._central_widget: QWidget = QWidget()
        self.setCentralWidget(self._central_widget)
        
        # Create layout
        self._central_layout: QGridLayout = QGridLayout()
        self._central_widget.setLayout(self._central_layout)
        
        # Add widgets
        self._central_layout.addWidget(self._tab_widget, 0, 0, 1, 2)
        self._central_layout.addWidget(self._status_bar, 1, 0, 1, 1)
        self._central_layout.addWidget(self._status_bar_button, 1, 1, 1, 1)
        
        
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

        self._root_buttons_layout.addWidget(self._file_label)
        
        
    def _create_browser_grid_layout(self) -> None:
        
        # Create widget
        self._browser_grid_widget: QWidget = QWidget()
        self._browser_main_layout.addWidget(self._browser_grid_widget)
        
        # Create layout
        self._browser_grid_layout: QGridLayout = QGridLayout()
        self._browser_grid_layout.setContentsMargins(0,0,0,0)
        self._browser_grid_widget.setLayout(self._browser_grid_layout)
        
        # Add widgets
        self.TREE_SIZE: tuple = 7, 2
        self.LIST01_SIZE: tuple = 1, 1
        self.LIST02_SIZE: tuple = 1, 1
        self.LIST03_SIZE: tuple = 1, 1
        self.TABLE_SIZE: tuple = 5, 3
        
        self._browser_grid_layout.addWidget(self._tree_widget, 0, 0, *self.TREE_SIZE)
        self._browser_grid_layout.addWidget(self._list_01, 0, self.TREE_SIZE[1], *self.LIST01_SIZE)
        self._browser_grid_layout.addWidget(self._list_02, 0, self.TREE_SIZE[1]+self.LIST01_SIZE[1], *self.LIST02_SIZE)
        self._browser_grid_layout.addWidget(self._list_03, 0, self.TREE_SIZE[1]+self.LIST01_SIZE[1]+self.LIST02_SIZE[1], *self.LIST03_SIZE)
        self._browser_grid_layout.addWidget(self._table_widget, self.LIST01_SIZE[0], self.TREE_SIZE[1], *self.TABLE_SIZE)
        

    def _create_settings_central_layout(self) -> None:
        
        # Create widget
        self._settings_tab: QWidget = QWidget()
        self._tab_widget.addTab(self._settings_tab, 'Settings')

        # Create layout
        self._settings_main_layout: QVBoxLayout = QVBoxLayout()
        self._settings_main_layout.setContentsMargins(0,0,0,0)
        self._settings_tab.setLayout(self._settings_main_layout)

        # Add widgets
        self._settings_main_layout.addWidget(self._settings_widget)

    
    # ------------------------------------------------------------------------------------------------------
    def _create_connections(self) -> None:
        
        for root_button in self._root_buttons:
            root_button.clicked.connect(self._update_current_path)
            root_button.clicked.connect(
                partial(self._populate_widget, widget=self._tree_widget)
            )
            
        self._tree_widget.itemClicked.connect(self._update_current_path)
        self._tree_widget.itemClicked.connect(
            partial(self._populate_widget, widget=self._list_01)
        )
        self._tree_widget.itemClicked.connect(
            partial(self._populate_widget, widget=self._table_widget)
        )
        
        self._list_01.itemClicked.connect(self._update_current_path)
        self._list_01.itemClicked.connect(
            partial(self._populate_widget, widget=self._list_02)
        )
        self._list_01.itemClicked.connect(
            partial(self._populate_widget, widget=self._table_widget)
        )
        
        self._list_02.itemClicked.connect(self._update_current_path)
        self._list_02.itemClicked.connect(
            partial(self._populate_widget, widget=self._list_03)
        )
        self._list_02.itemClicked.connect(
            partial(self._populate_widget, widget=self._table_widget)
        )
        
        self._list_03.itemClicked.connect(self._update_current_path)
        self._list_03.itemClicked.connect(
            partial(self._populate_widget, widget=self._table_widget)
        )
        
        self._table_widget.itemClicked.connect(self._update_current_path)

        self._status_bar_button.clicked.connect(self.copy_to_clipboard)
        self._settings_widget.project_button.clicked.connect(self.change_current_project)
        self.menu_bar.username_widget.button.clicked.connect(self.update_username)
        
    # ------------------------------------------------------------------------------------------------------
    def copy_to_clipboard(self) -> None:
        clipboard = QApplication.clipboard()
        clipboard.setText(str(self.current_path))


    def update_username(self) -> None:
        dialog: widgets.UsernameDialog = widgets.UsernameDialog(self)
        dialog.exec_()
        self.menu_bar.username_widget.button.setText(dialog.USERNAME)
        #self.menu_bar.username_widget.button.setMinimumSize(self.menu_bar.username_widget.button.sizeHint())

    
    def _auto_clic_while_use(self) -> None:
        
        root_button: widgets.CheckableButton = self.sender()
        memo_list: list[str] = Core.prefs_paths().MEMO_PATH_JSONFILE.json_to_dict().get('last_paths')
        
        if not memo_list:
            return
        
        if str(root_button.pipeline_path) in memo_list:
            return
        
        for index, memo_path in enumerate(memo_list):
            
            if str(root_button.pipeline_path) in memo_path:
                root_button.setChecked(False)
                self.current_path = self._project_path
                self.auto_clic(memo_list, index=index)  
                break

    
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

        self._file_label.setVisible(True if self.current_path.is_file() else False)
        self._file_label.setText(self.current_path.name if self.current_path.is_file() else '')

    def _populate_widget(self,
                         item: Union[widgets.PipelineWidgetItem, None] = None, 
                         column: Union[int, None] = None, 
                         widget: Union[widgets.PipelineWidget, None] = None
                         ) -> None:
        
        reset_widgets = [self._list_01, self._list_02, self._list_03, self._table_widget]

        if widget is self._tree_widget:
            for w in reset_widgets:
                w.populate_update_path(None)
            widget.populate_update_path(self.current_path)
            return

        if widget in reset_widgets:
            widget_index = reset_widgets.index(widget)
            for w in reset_widgets[widget_index+1:]:
                w.populate_update_path(None)
            widget.populate_update_path(self.current_path)
            return

        widget.populate_update_path(self.current_path)
            

    def update_memo_path(self) -> None:
        
        memo_path_jsonfile: JsonFile = Core.prefs_paths().MEMO_PATH_JSONFILE
        last_paths: list = memo_path_jsonfile.json_to_dict()['last_paths']
        
        if str(self.current_path) in last_paths:
            Logger.debug(f'Remove: {self.current_path}')
            last_paths.remove(str(self.current_path))
            
        else:
            match_path: Path = Core.find_root_dirpath(self.current_path, self._project_path)
            for path in last_paths:
                if str(match_path) in path or str(self.current_path) in path:
                    last_paths.remove(str(path))
                    break
        
        last_paths.insert(0, str(self.current_path))
        
        memo_path_jsonfile.dict_to_json({"last_paths": last_paths})
        Logger.debug(f'Memo path: {self.current_path}')
        
        
    def _auto_clic_widget(self, widget: widgets.PipelineWidget, next_widget: widgets.PipelineWidget, path: Path) -> None:
        
        column: int = 1 if isinstance(widget, widgets.TreeWidget) else 0
        
        for item in widget.iter_items():
            if path == item.pipeline_path:
                widget.setCurrentItem(item)
                self._update_current_path(item, column)
                self._populate_widget(item, column, next_widget)
                
        
    def auto_clic(self, last_paths: list[str], index: int = 0) -> None:
        
        if not last_paths:
            return
        
        all_paths: list[Path] = [Path(last_paths[index])]
        all_paths.extend(all_paths[0].parents)
        
        for parent in reversed(all_paths):
            
            for root_button in self._root_buttons:
                if parent == root_button.pipeline_path:
                    root_button.setChecked(True)
                    self.current_path = root_button.pipeline_path
                    self._status_bar.pipeline_path = root_button.pipeline_path
                    self.update_memo_path()
                    self._populate_widget(widget=self._tree_widget)
                    break
                    
            self._auto_clic_widget(self._tree_widget, self._list_01, parent)
            self._auto_clic_widget(self._list_01, self._list_02, parent)
            self._auto_clic_widget(self._list_01, self._table_widget, parent)
            self._auto_clic_widget(self._list_02, self._list_03, parent)
            self._auto_clic_widget(self._list_02, self._table_widget, parent)
            self._auto_clic_widget(self._list_03, self._table_widget, parent)


    def change_current_project(self) -> None:

        file_dialog: QFileDialog = QFileDialog()
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        file_dialog.setDirectory(str(self._project_path))
        new_project_path: Union[str, None] = file_dialog.getExistingDirectory(self, 'Select project path', options = QFileDialog.Options())

        if not new_project_path:
            return
        new_project_path = Path(new_project_path)

        if new_project_path.joinpath('.pinpin_data').exists():
            
            Core.prefs_paths().CURRENT_PROJECT_JSONFILE.set_value('current_project', str(new_project_path))
            self.project_path = new_project_path
            self._settings_widget.project_button.setText(self.project_path.name)
            Logger.info(f'Set projet: {self.project_path}')
            return
        
        shutil.copytree(
            Core.pinpin_path().joinpath('.pinpin_data'),
            new_project_path.joinpath('.pinpin_data')
        )
        
        dialog: widgets.SetPrefixDialog = widgets.SetPrefixDialog(self)
        if dialog.exec_() == dialog.Accepted:
            
            Core.prefs_paths().CURRENT_PROJECT_JSONFILE.set_value('current_project', str(new_project_path))
            self.project_path = new_project_path
            Core.project_data_paths().PREFIX_JSONFILE.set_value('prefix', dialog.PREFIX)
            self._settings_widget.project_button.setText(self.project_path.name)
            
            Logger.info(f'Set prefix: {dialog.PREFIX}')
            Logger.info(f'Set projet: {self.project_path}')
