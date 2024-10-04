from pathlib import Path
from PySide2.QtCore import QPoint, QSize, Qt
from PySide2.QtWidgets import QAbstractItemView, QAction, QMenu, QListWidget
from Packages.ui.new.widgets.list_widget_item import ListWidgetItem


class ListWidget(QListWidget):
    
    
    def __init__(self, path: Path, max_height: int = 100) -> None:
        super(ListWidget, self).__init__()
        
        self._pipeline_path: Path = path
        
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setFocusPolicy(Qt.NoFocus)
        self.setMaximumHeight(max_height)
        
        self._create_context_menu()
        self._create_connections()
        
        
    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
        
    @property
    def pipeline_name(self) -> str:
        return self._pipeline_path.name

    
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
        ...
        
        
    def _create_folder(self) -> None:
        ...


    def populate(self, path: Path) -> None:
        
        self.clear()
        self._pipeline_path = path
            
        for dirpath in self._pipeline_path.iterdir():
            
            if not dirpath.is_dir():
                continue
            
            item: ListWidgetItem = ListWidgetItem(self, dirpath)
