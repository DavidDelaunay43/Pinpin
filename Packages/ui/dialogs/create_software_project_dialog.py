import os
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog, QSizePolicy, QListWidget, QPushButton, QMenu, QAction, QGridLayout, QAbstractItemView
from Packages.logic.create_project import create_project
from Packages.ui.dialogs import TextEntryDialog
from Packages.ui.widgets import CustomListWidgetItem
from Packages.utils.constants import PINPIN_ICON_PATH, ICON_PATH

class SubFolderList(QListWidget):
    
    def __init__(self, parent = None, max_height = None):
        super(SubFolderList, self).__init__()
        
        self._create_context_menu()
        
    def _create_context_menu(self):
        """
        """
        
        self.context_menu = QMenu(self)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
        self.add_subfolder_action = QAction("Add sub folder", self)
        self.add_subfolder_action.triggered.connect(self.open_text_dialog)
        
        self.context_menu.addAction(self.add_subfolder_action)
        
    def _show_context_menu(self, pos):
        """
        """
        
        global_pos = self.mapToGlobal(pos)
        self.context_menu.exec_(global_pos)
        
    def open_text_dialog(self):
        
        text_dialog = TextEntryDialog(self, '', title = 'Add sub folder')
        if text_dialog.exec_() == QDialog.Accepted:
            entered_text = text_dialog.get_entered_text()
            print("Texte saisi : ", entered_text)

class CreateSoftProjectDialog(QDialog):
    def __init__(self, parent = None, directory: str = None):
        super().__init__(parent)

        self.DIRECTORY = directory

        self.setWindowTitle("Create software project")
        self.setWindowIcon(QIcon(PINPIN_ICON_PATH))
        self.setObjectName(u"create_soft_popup_container")
        self.resize(550, 270)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(550, 270))
        self.setMaximumSize(QSize(550, 270))
        self.setLayoutDirection(Qt.LeftToRight)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.create_widget()
        self.create_layout()
        self.create_connections()

        self.populate_list(self.soft_list, ['houdini', 'maya', 'nuke', 'zbrush'])
        
    def create_widget(self):
        # Create soft_list
        self.soft_list = QListWidget()
        self.soft_list.setObjectName(u"soft_list")
        soft_list_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        soft_list_policy.setHorizontalStretch(0)
        soft_list_policy.setVerticalStretch(0)
        soft_list_policy.setHeightForWidth(self.soft_list.sizePolicy().hasHeightForWidth())
        self.soft_list.setSizePolicy(soft_list_policy)
        self.soft_list.setMaximumHeight(200)
        self.soft_list.setTextElideMode(Qt.ElideNone)
        self.soft_list.setFocusPolicy(Qt.NoFocus)
        self.soft_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.sub_folder_list = SubFolderList()
        self.sub_folder_list.setObjectName(u"sub_folder_list")
        sub_folder_list_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sub_folder_list_policy.setHorizontalStretch(0)
        sub_folder_list_policy.setVerticalStretch(0)
        sub_folder_list_policy.setHeightForWidth(self.sub_folder_list.sizePolicy().hasHeightForWidth())
        self.sub_folder_list.setSizePolicy(sub_folder_list_policy)
        self.sub_folder_list.setMaximumHeight(200)
        self.sub_folder_list.setTextElideMode(Qt.ElideNone)
        self.sub_folder_list.setFocusPolicy(Qt.NoFocus)
        self.sub_folder_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.sub_folder_list.setSelectionMode(QListWidget.MultiSelection)
        
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.setMinimumSize(QSize(0, 40))

        self.apply_button = QPushButton("Apply")
        self.apply_button.setMinimumSize(QSize(0, 40))

    def create_layout(self):
        
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.soft_list, 0, 0)
        self.main_layout.addWidget(self.sub_folder_list, 0, 1)
        self.main_layout.addWidget(self.cancel_button, 1, 0)
        self.main_layout.addWidget(self.apply_button, 1, 1)

    def create_connections(self):
        '''
        '''
        
        self.apply_button.clicked.connect(self.create_soft_folder)
        self.soft_list.itemClicked.connect(self.populate_workspace_list)
        
        self.cancel_button.clicked.connect(self.reject)

    def populate_list(self, list_widget: QListWidget, items):
        '''
        '''
        
        for soft in items:
            
            item = CustomListWidgetItem(soft, list_widget)
            self._add_icon(item, soft) if list_widget == self.soft_list else None

    def populate_workspace_list(self, item):
        self.sub_folder_list.clear()
                
        soft_dict = {
            'houdini': ('scenes', 'geo', 'hda', 'sim', 'abc', 'tex', 'render', 'flip', 'scripts', 'comp', 'audio', 'video', 'desk'), 
            'maya': ('data', 'images', 'scenes', 'sourceimages', 'scripts', 'sound', 'clips', 'movies') ,
            'nuke': ('input', 'output'),
            'zbrush': None
        }
        
        software = item.text()
        sub_folders = soft_dict[software]
        self.populate_list(self.sub_folder_list, sub_folders) if sub_folders else None
        
    def create_soft_folder(self):

        SOFT_FOLDER = self.soft_list.selectedItems()
        if not SOFT_FOLDER or len(SOFT_FOLDER) == 0:
            return

        PARENT_DIRECTORY_NAME = SOFT_FOLDER[0].text()
        print(f'Create {PARENT_DIRECTORY_NAME} project in directory : {self.DIRECTORY}')

        WORKSPACE_FOLDER_LIST = [item.text() for item in self.sub_folder_list.selectedItems()]
        print(f'    workspace folders : {WORKSPACE_FOLDER_LIST}')

        create_project(self.DIRECTORY, PARENT_DIRECTORY_NAME, WORKSPACE_FOLDER_LIST)
        self.close()
            
    def _add_icon(self, widget, text="", bw: bool = True):
        '''
        '''
        
        bw_dict = {True: '_bw', False: ''}
        
        icon_file_path = os.path.join(ICON_PATH, f'{text.lower()}{bw_dict[bw]}_icon.ico')
        icon = QIcon(icon_file_path)
        widget.setIcon(icon)
