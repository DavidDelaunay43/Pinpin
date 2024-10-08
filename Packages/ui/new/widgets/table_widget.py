from pathlib import Path
from subprocess import Popen
from typing import Callable, Union
from PySide2.QtCore import QPoint, Qt
from PySide2.QtCore import Qt, QEvent, QObject
from PySide2.QtWidgets import QAbstractItemView, QAction, QHeaderView, QMenu, QTableWidget, QTableWidgetItem, QToolTip
from Packages.ui.new.widgets.input_dialog_multi_line import InputDialogMultiLine
from Packages.ui.new.widgets.input_dialog import InputDialog
from Packages.ui.new.widgets.table_widget_item import TableWidgetItem
from Packages.utils.core import Core
from Packages.utils.file_info import FileInfo
from Packages.utils.logger import Logger


class TableWidget(QTableWidget):
    
    
    def __init__(self, path: Union[Path, None] = None) -> None:
        super(TableWidget, self).__init__()
        
        self._pipeline_path: Union[Path, None] = path
        self._init_widget()
        self._create_context_menu()
        self._create_connections()
        
        self.setMouseTracking(True)
        self.viewport().installEventFilter(self)

                
    def _init_widget(self) -> None:
        self.setMinimumHeight(600)
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
        
        
    def connect_right_clic(self, function: Callable) -> None:
        self.customContextMenuRequested.connect(function)
        
        
    def eventFilter(self, source: QObject, event: QEvent):
        if source is self.viewport():
            if event.type() == event.ToolTip:
                item = self.itemAt(event.pos())
                if item:
                    QToolTip.showText(event.globalPos(), item.toolTip())
                else:
                    QToolTip.hideText()
            elif event.type() == event.Leave:
                QToolTip.hideText()
        return super().eventFilter(source, event)
    
        
    def _create_context_menu(self) -> None:
        
        self._context_menu: QMenu = QMenu()
        
        self._open_explorer_action: QAction = QAction('Open in explorer')
        self._create_folder_action: QAction = QAction('Increment file')
        self._edit_comment_action: QAction = QAction('Edit comment')
        self._invert_sort_action: QAction = QAction('Invert sort')
        self._max_files_action: QAction = QAction('Max files')
        
        self._open_explorer_action.triggered.connect(self._open_explorer)
        self._create_folder_action.triggered.connect(self._increment_file)
        self._edit_comment_action.triggered.connect(self._edit_comment)
        self._invert_sort_action.triggered.connect(self._invert_sort)
        self._max_files_action.triggered.connect(self._set_max_files)
        
        self._context_menu.addAction(self._open_explorer_action)
        self._context_menu.addAction(self._create_folder_action)
        self._context_menu.addAction(self._edit_comment_action)
        self._context_menu.addSeparator()
        self._context_menu.addAction(self._invert_sort_action)
        self._context_menu.addAction(self._max_files_action)
        
    
    def _create_connections(self) -> None:
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
    
    def _show_context_menu(self, pos: QPoint) -> None:
        self._context_menu.exec_(self.mapToGlobal(pos))
        
        
    def _open_explorer(self) -> None:
        Popen(['explorer', self.pipeline_path])
        
        
    def _increment_file(self) -> None:
        ...
        
    
    def _edit_comment(self) -> None:
        
        input_dialog: InputDialogMultiLine = InputDialogMultiLine(self, 'Edit Comment', 'Enter comment:')
        
        if input_dialog.exec_() != InputDialogMultiLine.Accepted:
            return
            
            
    def _invert_sort(self) -> None:
        invert_sort: bool = Core.prefs_paths().UI_PREFS_JSONFILE.get_value('reverse_sort_file')
        Core.prefs_paths().UI_PREFS_JSONFILE.set_value('reverse_sort_file', not invert_sort)
        if invert_sort:
            self.sortItems(1, Qt.AscendingOrder)
        else:
            self.sortItems(1, Qt.DescendingOrder)
        
        
    def _set_max_files(self) -> None:
        
        max_files: int = Core.prefs_paths().UI_PREFS_JSONFILE.get_value('num_files')
        
        input_dialog: InputDialog = InputDialog(self, 'Edit max files', 'Enter num:')
        
        if input_dialog.exec_() != InputDialog.Accepted:
            return
        
        num: int = input_dialog.textValue()
        if not num:
            return
        
        try:
            num = int(num)
        except ValueError as value_error:
            Logger.error(f'{value_error}')
            return
        
        Core.prefs_paths().UI_PREFS_JSONFILE.set_value('num_files', num)
        Logger.debug(f'Set max files: {num}')
        self.populate(self.pipeline_path)
    
    
    def populate_update_path(self, path: Union[Path, None]) -> None:
        self.pipeline_path = path
        self.populate(path)
    
    
    def populate(self, path: Union[Path, None]) -> None:
        
        invert_sort: bool = Core.prefs_paths().UI_PREFS_JSONFILE.get_value('reverse_sort_file')
        max_files: int = Core.prefs_paths().UI_PREFS_JSONFILE.get_value('num_files')
        
        self.setRowCount(0)
        if not path or path.is_file():
            return
        
        if not invert_sort:
            subdirs: list = list(path.iterdir())
        
        else:
            subdirs: list = list(reversed(list(path.iterdir())))
            
        subdirs = subdirs[:max_files] if len(subdirs) > max_files else subdirs
        
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
