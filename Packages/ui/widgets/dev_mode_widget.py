import os
from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtGui import Qt
from PySide2.QtWidgets import *
from Packages.logic.json_funcs import json_to_dict, dict_to_json
from Packages.logic.file_opener import FileOpener
from Packages.utils.constants import APPS_JSON_PATH,PREFS
from Packages.logic.filefunc import open_explorer
        
class devModeWidget(QWidget):
    
    def __init__(self, parent = None, file_directory = None) -> None:
        super(devModeWidget, self).__init__(parent)
        
        self.application = None
        self.prefs_directory = None
        self.create_widget()
        self.create_layout()
        self.create_connections()
        
    def create_widget(self):

        self.path_label=QLabel()
        self.path_label.setText("dev mode !")
    
        self.prefs_button = QPushButton()
        self.prefs_button.setObjectName("prefs_button")
        self.prefs_button.setFocusPolicy(Qt.NoFocus)
        self.prefs_button.setMaximumSize(QSize(150, 50))
        self.prefs_button.setMinimumSize(QSize(50, 50))
        self.prefs_button.setText("change maya preferences")

        self.open_pinpin_user_button = QPushButton()
        self.open_pinpin_user_button.setObjectName("open_pinpin_user_button")
        self.open_pinpin_user_button.setFocusPolicy(Qt.NoFocus)
        self.open_pinpin_user_button.setMaximumSize(QSize(150, 50))
        self.open_pinpin_user_button.setMinimumSize(QSize(50, 50))
        self.open_pinpin_user_button.setText("open .pinpin")
        

    def create_layout(self):
        self.setMinimumSize(QSize(50, 50))
        self._main_layout = QHBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._main_layout)
        
        self._main_layout.addWidget(self.path_label)
        self._main_layout.addWidget(self.prefs_button)
        self._main_layout.addWidget(self.open_pinpin_user_button)

        

    def create_connections(self):
        self.prefs_button.clicked.connect(self.set_pref)
        self.open_pinpin_user_button.clicked.connect(self.open_pinpin_user)

#utils -----------------------------------------------------------------------------
   
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

    def open_pinpin_user(self):
        dir = PREFS
        open_explorer(os.path.dirname(dir))
        
        

