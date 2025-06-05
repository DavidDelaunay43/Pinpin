from pathlib import Path
from subprocess import Popen
from typing import Callable, Union
from PySide2.QtCore import QPoint, Qt
from PySide2.QtWidgets import QAbstractItemView, QAction, QMenu, QListWidget
from Packages.ui.new.widgets.input_dialog import InputDialog
from Packages.ui.new.widgets.list_widget_item import ListWidgetItem
from Packages.utils.logger import Logger


class ListWidget(QListWidget):
    
    
    def __init__(self, path: Union[Path, None] = None, max_height: int = 100) -> None:
        super(ListWidget, self).__init__()
        
        self._pipeline_path: Union[Path, None] = path
        
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setFocusPolicy(Qt.NoFocus)
        self.setMaximumHeight(max_height)
        
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
    
    
    def connect_right_clic(self, function: Callable) -> None:
        self.customContextMenuRequested.connect(function)
    
    
    def populate_update_path(self, path: Union[Path, None]) -> None:
        self.pipeline_path = path
        self.clear()
        if path:
            self.populate()

    
    def _create_context_menu(self) -> None:
        
        self._context_menu: QMenu = QMenu()
        
        self._open_explorer_action: QAction = QAction('Open in explorer')
        self._create_folder_action: QAction = QAction('Create folder')
        
        self._open_explorer_action.triggered.connect(self._open_explorer)
        self._create_folder_action.triggered.connect(self._create_folder)
        
        self._context_menu.addAction(self._open_explorer_action)
        self._context_menu.addAction(self._create_folder_action)
        
    
    def _create_connections(self) -> None:
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
    
    def _show_context_menu(self, pos: QPoint) -> None:
        self._context_menu.exec_(self.mapToGlobal(pos))
        
        
    def _open_explorer(self) -> None:
        import platform
        import distro

        if platform.system().lower() == "windows":
            explorer = "explorer"
        elif platform.system().lower() == "linux":
            if distro.id().lower() == "rocky":
                explorer = "dolphin"

        Popen([explorer, self.pipeline_path])
        
    
    def _create_folder(self) -> None:
        
        input_dialog: InputDialog = InputDialog(self, 'Create Folder', 'Enter folder name:')
        
        if input_dialog.exec_() != InputDialog.Accepted:
            return
    
        dirname: str = input_dialog.textValue()
        if not dirname:
            return
        item_path: Path = self.pipeline_path.joinpath(dirname)
        ListWidgetItem(self, item_path)
        item_path.mkdir(parents=True, exist_ok=True)
        Logger.info(f'Create directory: {self._pipeline_path.joinpath(dirname)}')


    def populate(self) -> None:
        
        for dirpath in self._pipeline_path.iterdir():
            
            if not dirpath.is_dir():
                continue
            
            ListWidgetItem(self, dirpath)
            
            
    def iter_items(self) -> list[ListWidgetItem]:
        return [self.item(i) for i in range(self.count())]
    