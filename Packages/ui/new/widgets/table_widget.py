from pathlib import Path
from typing import Union
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem
from Packages.ui.new.widgets.table_widget_item import TableWidgetItem
from Packages.utils.file_info import FileInfo
from Packages.utils.logger import Logger


class TableWidget(QTableWidget):
    
    
    def __init__(self, path: Union[Path, None] = None) -> None:
        super(TableWidget, self).__init__()
        
        self._pipeline_path: Union[Path, None] = path
        
        self.setMouseTracking(True)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setShowGrid(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.horizontalHeader().setCascadingSectionResizes(False)
        self.horizontalHeader().setDefaultSectionSize(150)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setStretchLastSection(False)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setCascadingSectionResizes(False)
        self.verticalHeader().setHighlightSections(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setColumnCount(4)
        
        for index, column in enumerate(['Image', 'Version', 'Comment','Infos']):
            
            row = QTableWidgetItem()
            self.setHorizontalHeaderItem(index, row)
            self.horizontalHeaderItem(index).setText(column)
            
            try:
                self.setColumnWidth(index, [200, 50, None, 100][index])
            except:
                self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)
        
        
    @property
    def pipeline_path(self) -> Union[Path, None]:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Union[Path, None]) -> None:
        self._pipeline_path = path
        
        
    @property
    def pipeline_name(self) -> Union[str, None]:
        self._pipeline_path.name if self._pipeline_path else None
        
    
    def populate_update_path(self, path: Union[Path, None]) -> None:
        self.pipeline_path = path
        self.populate(path)
    
    
    def populate(self, path: Union[Path, None], reverse: bool = True) -> None:
        
        self.setRowCount(0)
        if not path or path.is_file():
            return
        
        if not reverse:
            subdirs: list = list(path.iterdir())
        
        else:
            subdirs: list = reversed(list(path.iterdir()))
        
        for file_path in subdirs:
            
            if file_path.is_dir():
                continue
            
            self._add_row(file_path=file_path)
        
    
    def _add_row(self, file_path: Path) -> None:
        
        file_info: FileInfo = FileInfo(file_path)
        Logger.debug(f'File info: {file_path.name}\nVersion: {file_info.version}\nComment: {file_info.comment}\nLast user: {file_info.last_user}')
        
        row_position: int = self.rowCount()
        self.insertRow(row_position)
        self.setRowHeight(row_position, 101)
        
        self.setItem(row_position, 0, TableWidgetItem(file_path, 'No preview')) # preview
        self.setItem(row_position, 1, TableWidgetItem(file_path, file_info.version, size=12)) # version
        self.setItem(row_position, 2, TableWidgetItem(file_path, file_info.comment)) # comment
        self.setItem(row_position, 3, TableWidgetItem(file_path, file_info.info_format)) # info
