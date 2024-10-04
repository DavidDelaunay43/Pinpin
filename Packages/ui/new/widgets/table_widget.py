from pathlib import Path
from PySide2.QtCore import Qt
from PySide2.QtWidgets import * 


class TableWidget(QTableWidget):
    
    
    def __init__(self, path: Path) -> None:
        super(TableWidget, self).__init__()
        
        self._pipeline_path: Path = path
        
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
        
        for index, column in enumerate('Image', 'Version', 'Comment','Infos'):
            
            row = QTableWidgetItem()
            self.setHorizontalHeaderItem(index, row)
            self.horizontalHeaderItem(index).setText(column)
            
            try:
                self.setColumnWidth(index, [200, 50, None, 100][index])
            except:
                self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)
        
        
    @property
    def pipeline_path(self) -> Path:
        return self._pipeline_path
    
    
    @pipeline_path.setter
    def pipeline_path(self, path: Path) -> None:
        self._pipeline_path = path
        
        
    @property
    def pipeline_name(self) -> str:
        self._pipeline_path.name
        
        
    def _add_row(self) -> None:
        ...
