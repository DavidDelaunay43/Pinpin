import os
import concurrent.futures
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QIcon
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from Packages.logic.filefunc import get_version_num, get_file_modification_date_time
from Packages.logic.json_funcs import get_file_data
from Packages.logic.filefunc import get_files
from Packages.ui.widgets.image_widget import ImageWidget
from Packages.utils.funcs import get_size, forward_slash
from Packages.utils.constants import ICON_PATH, UI_PREFS_JSON_PATH
from Packages.utils.funcs import get_current

class CustomTableWidget(QTableWidget):
    
    def __init__(self, parent = None):
        super(CustomTableWidget, self).__init__(parent)

        self.setMouseTracking(True)
        self.itemEntered.connect(self.showFileNameOnHover)

    def showFileNameOnHover(self, item):
        if item is not None:
            file_path = item.data(32)  # Récupérer le "nom de fichier" depuis le data
            if not file_path:
                return
            file_name = os.path.basename(file_path)
            tooltip_text = f'<span style="font-size: 20px; background-color: white; color: black; border: 0px transparent;">{file_name}</span>'
            self.setToolTip(tooltip_text)  # Afficher le "nom de fichier" dans un tooltip
    
    def set_table(self, columns: list, widths: list):
        """
        Example :
        self.set_table(['Image', 'Version', 'Comment','Infos'], [200, 50, None, 100])
        """
        
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
        
        column_count = len(columns)
        self.setColumnCount(column_count)
        
        for index, column in enumerate(columns):
            
            row = QTableWidgetItem()
            self.setHorizontalHeaderItem(index, row)
            self.horizontalHeaderItem(index).setText(column)
            
            try:
                self.setColumnWidth(index, widths[index])
            except:
                self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)

    def add_item(self, filepath: str, parallel: bool = True):
        """
        """
        
        filepath = forward_slash(filepath)
        filename = os.path.basename(filepath)
        
        row_position = self.rowCount()
        self.insertRow(row_position)
        self.setRowHeight(row_position, 101)
        
        # Create items
        
        # 0
        def _image_item():
            img_exts = ['.png', '.jpg', '.tex', '.exr']
            ext = os.path.splitext(filename)[-1]
            
            image_item = ImageWidget(filepath = filepath, image = ext in img_exts)
            image_item.setData(32, filepath)
            return image_item
        
        # 1
        def _version_item():
            version_item = QTableWidgetItem()
            version_item.setData(32, filepath)
            version_item.setTextAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(12)
            version_item.setFont(font)
            version_item.setText(get_version_num(filename))
            
            if os.path.splitext(filename)[-1] == '.usd':
                self._add_icon(version_item, 'usd')
            return version_item
        
        # 2
        def _comment_item():
            comment_item = QTableWidgetItem()
            comment_item.setData(32, filepath)
            #comment_item.setTextAlignment(Qt.AlignCenter)
            comment_data = get_file_data(filepath)['comment']
            comment_item.setText(comment_data)
            return comment_item
        
        # 3
        def _user_item():
            user_item = QTableWidgetItem()
            user_item.setData(32, filepath)
            user_item.setTextAlignment(Qt.AlignCenter)
            user_data = f"{get_file_data(filepath)['user']}\n{get_file_modification_date_time(filepath)}\n{get_size(filepath)}"
            user_item.setText(user_data)
            return user_item
        
        if parallel:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Exécuter les blocs en parallèle
                version_item = executor.submit(_version_item)
                comment_item = executor.submit(_comment_item)
                user_item = executor.submit(_user_item)
                
                version_item = version_item.result()
                comment_item = comment_item.result()
                user_item = user_item.result()
            
            image_item = _image_item()
            
        else:  
            image_item = _image_item()
            version_item = _version_item()
            comment_item = _comment_item()
            user_item = _user_item()
            
        self.setCellWidget(row_position, 0, image_item)
        self.setItem(row_position, 1, version_item)
        self.setItem(row_position, 2, comment_item)
        self.setItem(row_position, 3, user_item)
        
    def update_file_items(self, directory):
        '''
        '''

        self.setRowCount(0)
        
        if isinstance(directory, str):
            file_list = get_files(directory)
            
            if not file_list:
                return

            if get_current(UI_PREFS_JSON_PATH, 'reverse_sort_file'):
                file_list = sorted(file_list, reverse = True)
            file_list = file_list[:get_current(UI_PREFS_JSON_PATH, 'num_files')]
            
            if not file_list:
                return
            
            file_path_list = [os.path.join(directory, file) for file in file_list]
            
        elif isinstance(directory, list):
            file_path_list = directory
            
        else:
            raise TypeError('wrong argument.')
        
        

        for file_path in file_path_list:
            self.add_item(file_path)
            
    def _add_icon(self, widget, text="", bw: bool = False):
        '''
        '''
        
        bw_dict = {True: '_bw', False: ''}
        
        icon_file_path = os.path.join(ICON_PATH, f'{text.lower()}{bw_dict[bw]}_icon.ico')
        if not os.path.exists(icon_file_path):
            return
        
        icon = QIcon(icon_file_path)
        widget.setIcon(icon)
      