import os
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QTabWidget,QWidget,QVBoxLayout,QSizePolicy, QLineEdit,
                               QHBoxLayout,QAction,QMenu,QSplitter,QDialog,QTreeWidgetItem,
                               QListWidgetItem,QPushButton,QButtonGroup)

from Packages.utils.constants import ICON_PATH, PROJECT_JSON_PATH
from Packages.ui.dialogs import ProjectDialog, TextEntryDialog, CreateSoftProjectDialog
from Packages.ui.widgets import (StatusBar, CustomListWidget, CustomTableWidget, CustomListWidgetItem, 
                                 CustomMenuBar, CustomMainWindow, CustomTreeWidget
                                 )
from Packages.logic.json_funcs import (get_current_project_name, get_current_project_path, 
                                       get_file_data, update_file_data,
                                       set_clicked_item, set_clicked_radio_button, get_clicked_radio_button, get_clicked_item
                                       )
from Packages.logic.filefunc import clean_directory, open_explorer, increment_file_external
from Packages.logic.file_opener import FileOpener
from Packages.utils.logger import init_logger

logger = init_logger(__file__)

class BaseMainWindow(CustomMainWindow):
    """
    """
    def __init__(self, parent = None, set_style: bool = False):
        super(BaseMainWindow, self).__init__(parent, set_style)

        self.PARENT = parent
        self.PROJECT_NAME = get_current_project_name(PROJECT_JSON_PATH)
        self.PROJECT_PATH = get_current_project_path(PROJECT_JSON_PATH)
        self.set_display_basics(project = self.PROJECT_NAME)
        self._ensure_project()
        self.current_directory = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.create_context_menu()

        self.setMenuBar(CustomMenuBar(self))
        self.status_bar = StatusBar(parent = self._central_layout, text = self.PROJECT_PATH)
        self.auto_clic()
        self.show()
        self._get_active_tab_text()
     
    # UI
    def create_widgets(self):
        """
        """
        # BROWSER TAB --------------------------------------------------------------------------------------
        self.button_group = QButtonGroup()

        def create_checkable_button(button_text):
            checkable_button=QPushButton(button_text)
            checkable_button.setCheckable(True)
            checkable_button.setMinimumSize(60,35)
            checkable_button.setObjectName(f"checkable_button")
            self.button_group.addButton(checkable_button)
            return checkable_button
            
        self._asset_radio_button = create_checkable_button("Asset")
        self._sequence_radio_button = create_checkable_button('Sequence')
        self._shot_radio_button = create_checkable_button('Shot')
        self._publish_radio_button = create_checkable_button('Publish')
        self._texture_radio_button = create_checkable_button('Texture')
        self._cache_radio_button = create_checkable_button('Cache')
        self._rd_radio_button = create_checkable_button('Test')
        self._ressource_radio_button = create_checkable_button('Ressource')

        self.checkable_buttons = (
            self._asset_radio_button, 
            self._sequence_radio_button, 
            self._shot_radio_button,
            self._publish_radio_button,
            self._texture_radio_button,
            self._cache_radio_button,
            self._rd_radio_button,
            self._ressource_radio_button
        )

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("")
        self.search_bar.textChanged.connect(self.filter_items)
        self.tree_browser = CustomTreeWidget()

        self.list_01 = CustomListWidget( max_height=100)
        self.list_02 = CustomListWidget( max_height=100)
        self.list_03 = CustomListWidget( max_height=100)
        self.list_04 = CustomListWidget( max_height=100)

        self.list_01.create_context_menu(project_action = True)
        self.list_02.create_context_menu()
        self.list_03.create_context_menu()

        self._browser_file_table = CustomTableWidget()
        self._browser_file_table.set_table(['Image', 'Version', 'Comment','Infos'], [180, 100, None, 70])

        # RECENT TAB --------------------------------------------------------------------------------------
        self._recent_file_table = CustomTableWidget()
        self._recent_file_table.set_table(['Image', 'Version', 'Comment','Infos'], [180, 100, None, 70])

        # PUBLISH TAB -------------------------------------------------------------------------------------

    def create_layout(self):
        """
        """
        
        # Créer un QTabWidget
        self._tab_widget = QTabWidget()

        # Créer les 2 onglets
        self.browser_tab = QWidget()
        self.browser_tab.setObjectName("browser_tab")
        self.recent_tab = QWidget()
        self.recent_tab.setObjectName("recent_tab")

        # BROWSER TAB --------------------------------------------------------------------------------------
        # we create all the browser layout
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self._central_layout = QVBoxLayout()
        self._central_widget.setLayout(self._central_layout)

        self._browser_main_layout = QVBoxLayout()
        self._browser_main_layout.setContentsMargins(0, 0, 0, 0)
        
        self._browser_secondary_layout_widget=QWidget()
        self._browser_secondary_layout_widget.setObjectName("_browser_secondary_layout_widget")
        self._browser_secondary_layout = QHBoxLayout(self._browser_secondary_layout_widget)
        
        self._radio_layout_widget=QWidget()
        
        self._radio_layout_widget.setObjectName("_radio_layout_widget")
        self._radio_layout = QHBoxLayout(self._radio_layout_widget)
        self._radio_layout.setContentsMargins(10, 10, 10, 0)
        
        self._left_splitter = QSplitter(Qt.Vertical)
        self._left_splitter.setObjectName("_left_splitter")

        self._right_layout_widget=QWidget()
        self._right_layout_widget.setObjectName("_right_layout_widget")
        self._right_layout = QVBoxLayout(self._right_layout_widget)
        self._right_layout.setContentsMargins(0, 0, 0, 0)

        self._filter_layout_widget=QWidget()
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self._filter_layout_widget.setSizePolicy(size_policy)
        self._filter_layout = QHBoxLayout(self._filter_layout_widget)
        self._filter_layout.setContentsMargins(0, 0, 0, 0)

        self._browser_file_layout_widget = QWidget()
        self._browser_file_layout_widget.setObjectName("_file_layout_widget")
        self._browser_file_layout = QVBoxLayout(self._browser_file_layout_widget)
        self._browser_file_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tool_layout_widget = QWidget()
        self.tool_layout = QVBoxLayout(self.tool_layout_widget)

        # we fill each layout
        
        for radio_btn in self.checkable_buttons:
            self._radio_layout.addWidget(radio_btn)
        self._radio_layout.addStretch(1)
        
        #self._left_splitter.addWidget(self.search_bar)
        self._left_splitter.addWidget(self.tree_browser)
        self._left_splitter.addWidget(self.tool_layout_widget)

        self._browser_file_layout.addWidget(self._browser_file_table)

        self._filter_layout.addWidget(self.list_01)
        self._filter_layout.addWidget(self.list_02)
        self._filter_layout.addWidget(self.list_03)
        #self._filter_layout.addWidget(self.list_04)

        # we fill the window

        self._central_layout.addWidget(self._tab_widget)

        self._tab_widget.addTab(self.browser_tab, 'Browser')
        self._tab_widget.addTab(self.recent_tab, 'Recent')

        self.browser_tab.setLayout(self._browser_main_layout)
        self._browser_main_layout.addWidget(self._radio_layout_widget)
        self._browser_main_layout.addWidget(self._browser_secondary_layout_widget)
        
        self._right_layout.addWidget(self._filter_layout_widget)
        self._right_layout.addWidget(self._browser_file_layout_widget)
        self._browser_secondary_layout.addWidget(self._left_splitter)
        self._browser_secondary_layout.addWidget(self._right_layout_widget)
        
        # RECENT TAB --------------------------------------------------------------------------------------
        self._recent_main_layout = QVBoxLayout()
        self.recent_tab.setLayout(self._recent_main_layout)

        self._recent_file_layout_widget = QWidget()
        self._recent_file_layout_widget.setObjectName("_recent_file_layout_widget")
        self._recent_file_layout = QVBoxLayout(self._recent_file_layout_widget)
        self._recent_file_layout.setContentsMargins(0, 0, 0, 0)

        self._recent_file_layout.addWidget(self._recent_file_table)

        self._recent_main_layout.addWidget(self._recent_file_layout_widget)
        # PUBLISH TAB -------------------------------------------------------------------------------------

    def create_connections(self):
        """
        """

        for radio_button in self.checkable_buttons:
            radio_button.clicked.connect(self.on_radio_button_clicked)

        self._tab_widget.currentChanged.connect(self._on_tab_changed)

        self._browser_file_table.itemClicked.connect(self._on_file_item_clicked)
        self._recent_file_table.itemClicked.connect(self._on_file_item_clicked)
        
        self._browser_file_table.itemDoubleClicked.connect(self._open_file)
        self._recent_file_table.itemDoubleClicked.connect(self._open_file)

        self.tree_browser.itemClicked.connect(self.on_tree_item_clicked)

        self.list_01.create_project_action.triggered.connect(self._open_create_soft_project_dialog)
        self.list_01.create_folder_action.triggered.connect(self._open_create_folder_dialog_01)
        self.list_01.itemClicked.connect(self.on_list_item_clicked)
        self.list_02.create_folder_action.triggered.connect(self._open_create_folder_dialog_02)
        self.list_02.itemClicked.connect(self.on_list_item_clicked)
        self._select_item_from_text(self.list_02, 'scenes'.capitalize())
        self.list_03.create_folder_action.triggered.connect(self._open_create_folder_dialog_03)
        self.list_03.itemClicked.connect(self.on_list_item_clicked)
        self.list_04.itemClicked.connect(self.on_list_item_clicked)

    def create_context_menu(self):
        # Définir menu contextuel pour Comment
        self.context_menu = QMenu(self)
        
        self.edit_comment_action = QAction("Edit comment", self)
        self.file_dialog_action = QAction("Open in explorer", self)
        self.increment_file_action = QAction('Increment file', self)
        
        self.edit_comment_action.triggered.connect(self.open_comment_dialog)
        self.file_dialog_action.triggered.connect(self.open_file_dialog)
        self.increment_file_action.triggered.connect(self.increment_file)
        
        self.context_menu.addAction(self.edit_comment_action)
        self.context_menu.addAction(self.file_dialog_action)
        self.context_menu.addAction(self.increment_file_action)
        
        if self._get_active_radio_text() == 'Browser':
            self.context_menu.addAction(self.increment_file_action)
        
        self._browser_file_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._browser_file_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self._recent_file_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._recent_file_table.customContextMenuRequested.connect(self.show_context_menu_recent)

    def filter_items(self):
        # Filtrer les items du QTreeWidget en fonction du texte entré dans la barre de recherche
        filter_text = self.search_bar.text().lower()
        self.tree_browser.clearSelection()
        self.filter_items_recursive(self.tree_browser.invisibleRootItem(), filter_text)

    def filter_items_recursive(self, parent_item, filter_text):
        for index in range(parent_item.childCount()):
            item = parent_item.child(index)
            item_text = item.text(0).lower()
            if filter_text in item_text:
                item.setHidden(False)
                # Expand the parent items of the matching item
                self.expand_parent_items(item)
            else:
                item.setHidden(True)
            # Recursively filter child items
            self.filter_items_recursive(item, filter_text)

    def expand_parent_items(self, item):
        parent_item = item.parent()
        while parent_item:
            parent_item.setExpanded(True)
            parent_item = parent_item.parent()
    
    # AUTO-CLIC
    def auto_clic(self):
        '''
        '''
        text = get_clicked_radio_button()
        if not text:
            return
        
        for radio_btn in self.checkable_buttons:
            if text == radio_btn.text():
                radio_btn.setChecked(True)
                self.on_radio_button_clicked()
        
    # SLOTS
    def _get_active_tab_text(self):

        active_tab_index = self._tab_widget.currentIndex()
        tab_text = self._tab_widget.tabText(active_tab_index)

        return tab_text

    def _on_tab_changed(self, index):
        
        tab_text = self.sender().tabText(index)
        
        if tab_text == 'Recent':
            self.on_recent_tab_active()
            
        elif tab_text == 'Browser':
            self.on_browser_tab_active()
            
        else:
            pass
            
    def _get_last_clicked_list_item(self):
        lists = [self.list_01, self.list_02, self.list_03, self.list_04]

        for list_widget in lists:
            if list_widget.currentItem():
                return list_widget.currentItem()

        return None
    
    def on_browser_tab_active(self):
        self.status_bar.update(self.current_directory)
            
    def on_recent_tab_active(self):
        self.status_bar.update('')
    
    def _get_active_radio_text(self):
        return next((value.text() for value in self.checkable_buttons if value.isChecked()), None)
    
    def _click_tree_item_by_text(self, tree_widget: CustomTreeWidget, text_to_find: str, parent_item=None):
        if parent_item is None:
            # Si parent_item n'est pas spécifié, commencez la recherche depuis les éléments de niveau supérieur
            root_items = [tree_widget.topLevelItem(i) for i in range(tree_widget.topLevelItemCount())]
        else:
            # Sinon, commencez la recherche depuis les enfants de parent_item
            root_items = [parent_item]
        
        # Parcourez les éléments
        for item in root_items:
            if item.text(0) == text_to_find:  # Supposons que la colonne 0 contient le texte
                # Cliquez sur l'élément trouvé
                tree_widget.setCurrentItem(item)
                return True
            
            # Parcourez les enfants récursivement
            for column in range(item.columnCount()):
                for child_index in range(item.childCount()):
                    child_item = item.child(child_index)
                    if self._click_tree_item_by_text(tree_widget, text_to_find, child_item):
                        return child_item, column
        
        # Si l'élément n'a pas été trouvé, renvoie False
        return False
    
    def on_radio_button_clicked(self):

        self._add_base_folder_to_dir()
        self._fill_tree_items()
        radio_btn = self._get_active_radio_text()
        set_clicked_radio_button(self._get_active_radio_text())
        
        tree_item_text = get_clicked_item(radio_btn, 'tree_item')
        if not tree_item_text:
            return
        
        item, column = self._click_tree_item_by_text(self.tree_browser, tree_item_text)
        self.on_tree_item_clicked(item, column)
        
    def on_tree_item_clicked(self, item, column):
        
        self._add_tree_item_to_current_dir(item, column)
        self.populate_list_01(item, column)
        self.list_01.set_data(self.current_directory)
        
        if item.parent():
            set_clicked_item(self._get_active_radio_text(), 'tree_item', f'{item.text(column)}')
        
    def on_list_item_clicked(self, item):
        
        dico = {
            self.list_01: self.populate_list_02,
            self.list_02: self.populate_list_03,
            self.list_03: self.populate_list_04
        }
        
        self._add_dir(item)
        self.show_files()
        dico[item.listWidget()](None) # example : self.populate_list_02(None)

        logger.info(f'Item data : {item.data(32)}')
        logger.info(f'List data : {item.listWidget().data}')
        
        dico = {
            self.list_01: self.list_02,
            self.list_02: self.list_03
        }
        
        #
        if item.listWidget() == self.list_01:
            self.list_02.data = item.data(32)
            
        elif item.listWidget() == self.list_02:
            self.list_03.data = item.data(32)
            
        else:
            pass
    
    # CONNECTIONS
    def _open_file(self, item):
        
        file = item.data(32)
        FileOpener(file)

    def _fill_tree_items(self):
        self.tree_browser.clear()
        self.list_01.clear()
        self.list_02.clear()
        self.list_03.clear()
        self.list_04.clear()
        self._browser_file_table.setRowCount(0)


        # check if the path exist
        if os.path.exists(self.current_directory):
            
            for directory in os.listdir(self.current_directory):

                directory_path = os.path.join(self.current_directory, directory)
                if not os.path.isdir(os.path.join(self.current_directory, directory)): 
                    #print(os.path.join(self.current_directory, directory)+" is not a dir")#ATTENTION iici j'ai remplacé directory par os.path.join(self.current_directory, directory)
                    logger.warning(f'{os.path.join(self.current_directory, directory)} is not a directory.')
                    return

                root = QTreeWidgetItem(self.tree_browser)
                root.setText(0, directory)
                root.setFlags(root.flags() & ~Qt.ItemIsSelectable)
                
                for sub_directory in os.listdir(directory_path):
                    #print("sub  "+sub_directory)
                    sub_directory_path = os.path.join(directory_path, sub_directory)
                    #if not os.path.isdir(sub_directory_path): return #ATTENTION ici j'ai du caché une ligne, car sinon le if return car il trouve des fichier dans le .data
                    item = QTreeWidgetItem(root)
                    item.setText(0, sub_directory.capitalize())
        else:
            # The directory path does not exist, handle the error or take appropriate action
            logger.error(f"The path '{self.current_directory}' does not exist.")
    
    def populate_list_01(self, tree_item, column):
        if self.tree_browser.indexOfTopLevelItem(tree_item) != -1:
            self.list_01.clear()
            return
        
        self.list_01.clear()
        self.list_02.clear()
        self.list_03.clear()
        self.list_04.clear()
        
        for directory in os.listdir(self.current_directory):
            if not os.path.isdir(os.path.join(self.current_directory, directory)): continue
            
            #item = QListWidgetItem(directory.capitalize())
            item = CustomListWidgetItem(directory.capitalize(), self.list_01)
            self._add_icon(item, directory)
            item.setData(32, os.path.join(self.current_directory, directory))
            #self.list_01.addItem(item)
            
    def populate_list_02(self, parent_directory: str):
        
        self.list_02.clear()
        self.list_03.clear()
        self.list_04.clear()
        
        for directory in os.listdir(self.current_directory):
            if not os.path.isdir(os.path.join(self.current_directory, directory)): continue
            
            item = QListWidgetItem(directory.capitalize())
            self._add_icon(item, directory)
            item.setData(32, os.path.join(self.current_directory, directory))
            self.list_02.addItem(item)
        
        self._select_item_from_text(self.list_02, 'scenes'.capitalize()) #
        
    def populate_list_03(self, parent_directory: str):
        
        self.list_03.clear()
        self.list_04.clear()
        
        for directory in os.listdir(self.current_directory):
            if not os.path.isdir(os.path.join(self.current_directory, directory)): continue
            
            item = QListWidgetItem(directory.capitalize())
            self._add_icon(item, directory)
            item.setData(32, os.path.join(self.current_directory, directory))
            self.list_03.addItem(item)
        
    
    def populate_list_04(self, parent_directory: str):
        
        self.list_04.clear()
        self.populate_list_04_executed = False
        
        for directory in os.listdir(self.current_directory):
            if not os.path.isdir(os.path.join(self.current_directory, directory)): return
            
            item = QListWidgetItem(directory.capitalize())
            self._add_icon(item, directory)
            item.setData(32, os.path.join(self.current_directory, directory))
            self.list_04.addItem(item)
        
        #self.list_04.itemClicked.connect(self._add_dir)
                
    # UPDATE CURRENT DIRECTORY
    def _add_base_folder_to_dir(self):
        self.current_directory = self.PROJECT_PATH # je remets le DIR à la racine 
        self.current_directory = os.path.join(self.PROJECT_PATH, self._get_active_radio())
        self.status_bar.update(self.current_directory) # j'ajoute le dir 
                 
    def _add_tree_item_to_current_dir(self, item, column):
        
        text_to_add = f'{item.text(column)}'.lower()
        
        self.current_directory = os.path.join(self.PROJECT_PATH, self._get_active_radio())
        
        if not item.parent():
            self.current_directory = os.path.join(self.current_directory, text_to_add)
            
        else:
            self.current_directory = os.path.join(self.current_directory, item.parent().text(0), text_to_add)
             
        self.status_bar.update(self.current_directory)
        
        self._browser_file_table.setRowCount(0)
        self.show_files()
    
    def _add_dir(self, item):
        
        DIR = item.text().lower()
        LIST = item.listWidget()
        
        for i in range(LIST.count()):
            ITEM = LIST.item(i).text().lower()
            if ITEM in self.current_directory:
                self.current_directory = clean_directory(self.current_directory, ITEM)
                break
                
        self.current_directory = os.path.join(self.current_directory, DIR)
        self.status_bar.update(self.current_directory)

    # DIALOGS
    def _ensure_project(self):
        """
        """
        if self.PROJECT_NAME:
            pass
        else:
            self.dialog = ProjectDialog(parent=self)
            self.dialog.show()
            self.dialog.finished.connect(self.show)
            
    def _open_project_dialog(self):
        """
        """
        
        dialog = ProjectDialog(parent=self)
        dialog.show()
    
    def open_comment_dialog(self):
        
        file_path = self.status_bar.get_text()
        file_comment = get_file_data(file_path)['comment']
        logger.info(f'Get file infos : {file_path}')
        
        self.context_menu.close()
        dialog = TextEntryDialog(self, text = file_comment, title = 'Edit comment')
        
        if dialog.exec_() == QDialog.Accepted:
            entered_text = dialog.get_entered_text()
            logger.info(f'Texte saisi : {entered_text}')
            
            update_file_data(file_path, entered_text)
            
            if self._get_active_tab_text() == 'Browser':
                comment_item = self._browser_file_table.selectedItems()[1]
            else:
                comment_item = self._recent_file_table.selectedItems()[1]
            comment_item.setText(get_file_data(file_path)['comment'])
            
    def _open_create_soft_project_dialog(self):
        
        directory = self.list_01.data
        logger.info(f'directory arg : {directory}')
        logger.info('Open option dialog.')
        project_dialog = CreateSoftProjectDialog(self, directory = directory)
        project_dialog.exec_()
        
        self.on_radio_button_clicked()
        
    def _open_create_folder_dialog(self, list_widget):
        
        dialog = TextEntryDialog(self, text = '', title = 'Enter folder name')
        
        if dialog.exec_() == QDialog.Accepted:
            directory = list_widget.data
            logger.info(f'DIRECTORY : {directory}')
            folder_name = dialog.get_entered_text()
            logger.info(f'Texte saisi : {folder_name}')
            
            os.mkdir(os.path.join(directory, folder_name))
            self.on_radio_button_clicked()
        
    def _open_create_folder_dialog_01(self):
        self._open_create_folder_dialog(self.list_01)
            
    def _open_create_folder_dialog_02(self):
        self._open_create_folder_dialog(self.list_02)
        
    def _open_create_folder_dialog_03(self):
        self._open_create_folder_dialog(self.list_03)
            
    def open_file_dialog(self):
        """
        """
        
        if self._get_active_tab_text() == 'Browser':
            dir = self.current_directory
        else:
            dir = self.status_bar.get_text()
            
        open_explorer(os.path.dirname(dir))

    # UTILS
    def _get_active_radio(self):
        WORKFLOW_DICT = {
            self._asset_radio_button: "04_asset",
            self._sequence_radio_button: "05_sequence",
            self._shot_radio_button: "06_shot",
            self._publish_radio_button: "09_publish",
            self._texture_radio_button: "10_texture",
            self._cache_radio_button: "11_cache",
            self._rd_radio_button: "12_test",
            self._ressource_radio_button: "02_ressource"
        }
        
        return next((value for key, value in WORKFLOW_DICT.items() if key.isChecked()), None)

    def increment_file(self):
        increment_file_external(self.current_directory)
        self.current_directory = os.path.dirname(self.current_directory)
        self.show_files()
            
    def delete_file(self): # OBSOLETE
        os.remove(self.current_directory)
        
        selected_rows = self._browser_file_table.selectionModel().selectedRows()
        for row in selected_rows:
            self._browser_file_table.removeRow(row.row())
            
        self._on_file_item_clicked()
            
        # ATTENTION LA STATUS BAR N'est pas update

    def _add_icon(self, widget, text="", bw: bool = True):
        '''
        '''
        
        bw_dict = {True: '_bw', False: ''}
        
        icon_file_path = os.path.join(ICON_PATH, f'{text.lower()}{bw_dict[bw]}_icon.ico')
        if not os.path.exists(icon_file_path):
            return
        
        icon = QIcon(icon_file_path)
        widget.setIcon(icon)

    def show_files(self):
        logger.info('Show files - - - - - - - - - - - - - - - - - - - - - - - -')
        self._browser_file_table.update_file_items(self.current_directory)
        logger.info('End show files - - - - - - - - - - - - - - - - - - - - - - - -')
        
    def _add_file_to_table(self, filename):
        
        filepath = os.path.join(self.current_directory, filename)
        
        self._browser_file_table.add_item(filepath)
        
    def show_context_menu(self, pos):
        """
        """
        
        self._on_file_item_clicked(self._browser_file_table.itemAt(pos))
        
        global_pos = self._browser_file_table.mapToGlobal(pos)
        self.context_menu.exec_(global_pos)
        
    def show_context_menu_recent(self, pos):
        """
        """
        
        self._on_file_item_clicked(self._recent_file_table.itemAt(pos))
        
        global_pos = self._recent_file_table.mapToGlobal(pos)
        self.context_menu.exec_(global_pos)
    
    def _on_file_image_cliked(self, event):
        '''
        '''
        print('file image clicked')
    
    def _on_file_item_clicked(self, item):
        
        logger.info('file item clicked')
        
        file_path = item.data(32)

        if  self._get_active_tab_text() == 'Browser':
            self.current_directory = file_path
            self.status_bar.update(self.current_directory)
        else:
            self.status_bar.update(file_path)
        
    def _select_item_from_text(self, parent_widget, text = ""):
        
        dico = {
            self.list_01: self.populate_list_02,
            self.list_02: self.populate_list_03,
            self.list_03: self.populate_list_04,
        }
        
        for i in range(parent_widget.count()):
            
            item = parent_widget.item(i)
            
            if item.text() == text:
                
                parent_widget.setItemSelected(item, True)
                self._add_dir(item)
                dico[parent_widget](item)
                self.on_list_item_clicked(item) ########### attention à vérifier !!
                break
