from pathlib import Path
from subprocess import Popen
from typing import Union
from PySide2.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PySide2.QtWidgets import QAbstractItemView, QAction, QHeaderView, QMenu, QTableWidget, QTableWidgetItem, QToolTip
from Packages.ui.new.widgets.input_dialog_multi_line import InputDialogMultiLine
from Packages.ui.new.widgets.input_dialog import InputDialog
from Packages.ui.new.widgets.table_widget_item import TableWidgetItem
from Packages.utils.core import Core
from Packages.utils.file_info import FileInfo
from Packages.utils.json_file import JsonFile
from Packages.utils.logger import Logger


class TableWidget(QTableWidget):
    
    
    def __init__(self, parent = None, path: Union[Path, None] = None) -> None:
        super(TableWidget, self).__init__(parent)
        
        self._main_window = parent
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
        self.setIconSize(QSize(256, 144))
        
        for index, column in enumerate(['Image', 'Version', 'Comment','Infos']):
            
            row = QTableWidgetItem()
            self.setHorizontalHeaderItem(index, row)
            self.horizontalHeaderItem(index).setText(column)
            
            try:
                self.setColumnWidth(index, [136, None, None, 100][index])
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
        
        self._main_window._update_current_path(self.currentItem())
        self._context_menu.exec_(self.mapToGlobal(pos))
    
    
    def _open_explorer(self) -> None:
        Popen(['explorer', self.pipeline_path])
        
        
    def _increment_file(self) -> None:
        pipeline_path: Path = self.currentItem().pipeline_path
        file_info: FileInfo = FileInfo(pipeline_path)
        file_info.external_increment()
        
        row_pos_arg: Union[int, None] = 0 if Core.prefs_paths().UI_PREFS_JSONFILE.get_value('reverse_sort_file') else None
        self._add_row(file_info.NEXT_PIPELINE_PATH, row_pos=row_pos_arg)
        
    
    def _edit_comment(self) -> None:
        
        pipeline_path: Path = self.currentItem().pipeline_path
        file_info_jsonfile: JsonFile = Core.project_data_paths().FILE_DATA_JSONFILE
        
        all_file_info_dict: dict = file_info_jsonfile.json_to_dict()
        text: str = all_file_info_dict[str(pipeline_path)]['comment'] if str(pipeline_path) in all_file_info_dict.keys() else None
        
        input_dialog: InputDialogMultiLine = InputDialogMultiLine(self, 'Edit Comment', 'Enter comment:', text=text)
        
        if input_dialog.exec_() != InputDialogMultiLine.Accepted:
            return
            
        text = input_dialog.text
        if not text:
            return
        
        all_file_info_dict[str(pipeline_path)] = {'comment': text, 'user': Core.username()}
        file_info_jsonfile.dict_to_json(all_file_info_dict)
        self.selectedItems()[2].setText(text)
        Logger.info(f'Update comment:\nFile path: {pipeline_path}\nComment: {text}')
        
            
    def _invert_sort(self) -> None:
        invert_sort: bool = Core.prefs_paths().UI_PREFS_JSONFILE.get_value('reverse_sort_file')
        Core.prefs_paths().UI_PREFS_JSONFILE.set_value('reverse_sort_file', not invert_sort)
        if invert_sort:
            self.sortItems(1, Qt.AscendingOrder)
        else:
            self.sortItems(1, Qt.DescendingOrder)
        
        
    def _set_max_files(self) -> None:
        
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
        
    
    def _add_row(self, file_path: Path, row_pos: Union[int, None] = None) -> None:

        row_position: int = row_pos if row_pos == 0 else self.rowCount()
        self.insertRow(row_position)
        self.setRowHeight(row_position, 90)

        if len(file_path.name.split('_')) < 5:
            self.setItem(row_position, 0, TableWidgetItem(file_path, '*'))
            self.setItem(row_position, 1, TableWidgetItem(file_path, file_path.name, size=12))
            self.setItem(row_position, 2, TableWidgetItem(file_path, '*'))
            self.setItem(row_position, 3, TableWidgetItem(file_path, '*'))
            return
        
        file_info: FileInfo = FileInfo(file_path)
        Logger.debug(f'File info: {file_path.name}\nVersion: {file_info.version}\nComment: {file_info.comment}\nLast user: {file_info.last_user}')
        
        version: str = file_info.version if not file_info.parent_dirpath.name.lower()=='old' else f'{file_info.pipeline_name.split("_")[-4]}\n{file_info.version}'

        self.setItem(row_position, 0, TableWidgetItem(file_path, 'No preview', icon=file_info.preview_image_path)) # preview
        self.setItem(row_position, 1, TableWidgetItem(file_path, version, size=12)) # version
        self.setItem(row_position, 2, TableWidgetItem(file_path, file_info.comment)) # comment
        self.setItem(row_position, 3, TableWidgetItem(file_path, file_info.info_format)) # info
