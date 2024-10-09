from pathlib import Path
from subprocess import Popen
from typing import Callable, Union
from PySide2.QtCore import QPoint, QSize, Qt
from PySide2.QtWidgets import QAction, QMenu, QTreeWidget
from Packages.ui.new.widgets.input_dialog import InputDialog
from Packages.ui.new.widgets.tree_widget_item import TreeWidgetItem
from Packages.utils.logger import Logger


class TreeWidget(QTreeWidget):
    
    
    def __init__(self, path: Union[Path, None] = None):
        super(TreeWidget, self).__init__()
        
        self._pipeline_path: Union[Path, None] = path
        
        self.setMinimumWidth(250)
        self.setHeaderHidden(True)
        self.setTextElideMode(Qt.ElideNone)
        self.setAnimated(True)
        self.header().setVisible(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("font-size: 14px;")
        self.setIconSize(QSize(35, 35))
        
        self._create_context_menu()
        self._create_connections()
        
        
    @property
    def pipeline_path(self) -> Union[Path, None]:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
        

    @property
    def pipeline_name(self) -> Union[str, None]:
        return self._pipeline_path.name if self._pipeline_path else None
    
    
    def connect_right_clic(self, function: Callable) -> None:
        self.customContextMenuRequested.connect(function)
    
    
    def populate_update_path(self, path: Union[Path, None]) -> None:
        self.pipeline_path = path
        self.populate(path)
    
    
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
        item: TreeWidgetItem = self.currentItem()
        if item:
            Popen(['explorer', item.pipeline_path.parent])
        else:
            Popen(['explorer', self.pipeline_path])
        
        
    def _create_folder(self) -> None:
        item: TreeWidgetItem = self.currentItem()
        if item:
            parent_item: TreeWidgetItem = item.parent()
            item_size: list[int] = [40,40]
            parent_path: Path = item.pipeline_path.parent
            text: str = parent_item.pipeline_name.split('_')[-1]
        else:
            parent_item: TreeWidget = self
            item_size: None = None
            parent_path: Path = self.pipeline_path
            text: str = self.pipeline_name.split('_')[-1]
            
        input_dialog: InputDialog = InputDialog(self, f'Create {text.capitalize()}', f'Enter {text} name:')
        
        if input_dialog.exec_() == InputDialog.Accepted:
            dirname: str = input_dialog.textValue()
            if not dirname:
                return
            item_path: Path = parent_path.joinpath(dirname)
            item: TreeWidgetItem = TreeWidgetItem(parent_item, item_path, item_size)
            parent_path.joinpath(dirname).mkdir(parents=True, exist_ok=True)
            Logger.info(f'Create directory: {parent_path.joinpath(dirname)}')
    
    
    def iter_items(self) -> list[TreeWidgetItem]:
        
        return [
            root_item.child(i)
                for j in range(self.topLevelItemCount())
                for root_item in [self.topLevelItem(j)]
                for i in range(root_item.childCount())
        ]
    
    
    def populate(self, path: Union[Path, None]) -> None:
        
        self.clear()
        if not path:
            return
        
        for dirpath in self._pipeline_path.iterdir():
            
            if not dirpath.is_dir():
                continue
            
            root_item: TreeWidgetItem = TreeWidgetItem(self, dirpath)
            root_item.setFlags(root_item.flags() & ~Qt.ItemIsSelectable)
            
            for subdirpath in root_item.pipeline_path.iterdir():
                
                if not subdirpath.is_dir():
                    continue
                
                item: TreeWidgetItem = TreeWidgetItem(root_item, subdirpath, [40,40])
