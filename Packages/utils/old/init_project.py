import os
import shutil
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel, QFileDialog
from Packages.logic.json_funcs.convert_funcs import json_to_dict, dict_to_json
from Packages.utils.constants.preferences import CURRENT_PROJECT_JSON_PATH
from Packages.utils.constants.project_pinpin_data import BLANK_PINPIN_DATA, pinpin_data_PATH


class InitProject(QDialog):
    
    PROJECT = ''
    ACCEPTED = False
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.init_ui()
        self.create_connections()
    
    
    def init_ui(self) -> None:
        self.setWindowTitle('Select project')
        self.setMinimumSize(300, 150)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.button = QPushButton('Select your project.')
        self.label = QLabel('<project path>')
        self.ok_button = QPushButton('Apply')
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.ok_button)
        

    def create_connections(self) -> None:
        self.button.clicked.connect(self.select_project)
        self.ok_button.clicked.connect(self.set_project)


    def update_label(self, string: str) -> None:
        self.label.setText(string)
        
        
    def apply(self) -> None:
        current_project_dict: dict = json_to_dict(CURRENT_PROJECT_JSON_PATH)
        current_project_dict['current_project'] = self.label.text()
        dict_to_json(current_project_dict, CURRENT_PROJECT_JSON_PATH)
        self.check_pinpin_data()
        self.close()
    
    
    def check_pinpin_data(self) -> None:
        if not os.path.exists(pinpin_data_PATH):
            shutil.copytree(BLANK_PINPIN_DATA, pinpin_data_PATH)
            return
        
        
    def select_project(self) -> None:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        options = QFileDialog.Options()
        project_path: str = file_dialog.getExistingDirectory(self, 'Select directory', options=options)
        self.PROJECT = project_path.replace('\\', '/')
        self.update_label(string=self.PROJECT)
        
        
    def set_project(self) -> None:
        project_dict: dict = json_to_dict(CURRENT_PROJECT_JSON_PATH)
        project_dict['current_project'] = self.PROJECT
        dict_to_json(dictionary=project_dict, json_file_path=CURRENT_PROJECT_JSON_PATH)
        self.ACCEPTED = True
        self.accept()
