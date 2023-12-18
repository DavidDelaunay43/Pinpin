import os
from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QPushButton, QWidget, QHBoxLayout, QFileDialog
from Packages.logic.json_funcs import json_to_dict, dict_to_json
from Packages.logic.file_opener import FileOpener
from Packages.utils.constants import ICON_PATH, EXTS, APPS_JSON_PATH
        
class OpenFileWidget(QWidget):
    
    def __init__(self, parent = None, file_directory = None) -> None:
        super(OpenFileWidget, self).__init__(parent)
        
        self.application = None
        self.prefs_directory = None
        self._init_ui()
        self.update_buttons(file_directory)
        
    def _init_ui(self):
    
        self.setMinimumSize(QSize(50, 50))
        self._main_layout = QHBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self._main_layout)
        
        self.prefs_button = QPushButton()
        self.open_file_button = QPushButton()
        self.open_file_button.setObjectName("open_file_button")
        self.open_file_button.setFocusPolicy(Qt.NoFocus)
        self.open_file_button.setMaximumSize(QSize(10000, 50))
        self.open_file_button.setMinimumSize(QSize(50, 50))
        self.setStyleSheet('font-size: 16px;')

        self.prefs_button = QPushButton()
        self.prefs_button.setObjectName("prefs_button")
        self.prefs_button.setFocusPolicy(Qt.NoFocus)
        self.prefs_button.setMaximumSize(QSize(150, 50))
        self.prefs_button.setMinimumSize(QSize(50, 50))
        self.setStyleSheet('font-size: 16px;')

        self._main_layout.addWidget(self.prefs_button)
        self._main_layout.addWidget(self.open_file_button)

        self.prefs_button.clicked.connect(self.set_pref)
        
        
    def set_pref(self):
        
        file_dialog = QFileDialog()
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)  # Affiche uniquement les répertoires
        options = QFileDialog.Options()
        file_dialog.setDirectory(os.path.dirname(self.prefs_directory))
        pref_directory = file_dialog.getExistingDirectory(self, 'Sélectionner un répertoire', options=options)

        if not pref_directory: return
    
        app_dict = json_to_dict(APPS_JSON_PATH)
        app_dict[self.application]['pref'] = pref_directory
        dict_to_json(app_dict, APPS_JSON_PATH)
        self.prefs_button.setText(os.path.basename(pref_directory))
  
    def get_pref(self, application: str):
        if not application: return
        
        app_dict = json_to_dict(APPS_JSON_PATH)
        if not application in app_dict: return
        
        self.prefs_directory = app_dict[application]['pref']
        
    def set_text(self, application: str):
        
        # Open file button
        button_text = f'Open file in {application.capitalize()}' if application else ""
        self.open_file_button.setText(button_text)
        
        # Preferences button
        if application:
            if application == 'usdview':
                self.prefs_button.setText('')
            else:
                self.get_pref(application)
                self.prefs_button.setText(os.path.basename(self.prefs_directory))
        else:
            self.prefs_button.setText('')
        
    def set_icon(self, icon_name: str):
        
        if icon_name:
            icon_app_name = f'{icon_name}_icon.ico'
            icon_pref_name = 'folder_icon.ico'
        else:
            icon_app_name = 'none.ico'
            icon_pref_name = 'none.ico'
        
        icon_app_file_path = os.path.join(ICON_PATH, icon_app_name)
        icon_pref_file_path = os.path.join(ICON_PATH, icon_pref_name)
        
        icon_app = QIcon(icon_app_file_path)
        icon_pref = QIcon(icon_pref_file_path)
        
        self.open_file_button.setIcon(icon_app)
        self.prefs_button.setIcon(icon_pref)
        
        self.open_file_button.setIconSize(icon_app.actualSize(QSize(30,30)))
        self.prefs_button.setIconSize(icon_pref.actualSize(QSize(30,30)))
        
    def set_display(self, application: str):
        
        self.set_text(application)
        self.set_icon(application)
    
    def update_buttons(self, file_directory: str):
        
        try:
            extension = os.path.splitext(file_directory)[-1]
            if extension:
                self.application = EXTS[extension]
            else:
                self.application = ""
        except:
            self.application = None
        
        self.set_display(self.application)
    
    def open_file_in_app(self, directory: str):
        self.get_pref(self.application)
        FileOpener(directory, self.prefs_directory)
