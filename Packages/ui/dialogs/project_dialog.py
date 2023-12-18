import os
import json
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QPushButton, QHBoxLayout, QFileDialog

from Packages.logic.json_funcs import (set_current_project, 
                                       get_current_project_name, 
                                       get_current_project_path)
from Packages.logic.project_structure import ProjectStructure
from Packages.utils.constants import PROJECT_JSON_PATH


class ProjectDialog(QDialog):
    """
    """
    
    def __init__(self, parent=None):
        super(ProjectDialog, self).__init__(parent)
        
        self.parent = parent
        self.setWindowTitle('Project Dialog')
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        
        self._create_widgets()
        self._create_layout()
        self._create_connections()
        
    def _create_widgets(self):
        self.open_project_btn = QPushButton('Open Project')
        self.create_project_btn = QPushButton('Create Project')
    
    def _create_layout(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        
        self.main_layout.addWidget(self.open_project_btn)
        self.main_layout.addWidget(self.create_project_btn)
    
    def _create_connections(self):
        self.open_project_btn.clicked.connect(self._open_file_dialog)
    
    def _open_create_project_dialog(self):
        pass
    
    def _open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setWindowTitle("Ouvrir un projet existant")
        
        project_dir = file_dialog.getExistingDirectory(self, "Sélectionner le répertoire du projet", "", options=options)
        
        if project_dir:
                    
            set_current_project(project_dir)
            self.parent.project_name = get_current_project_name(PROJECT_JSON_PATH)
            self.parent.project_path = get_current_project_path(PROJECT_JSON_PATH)
            self.parent.project_structure = ProjectStructure(self.parent.project_path)
            self.parent.project_menu.setTitle(f'Project : {self.parent.project_name}')
            self.parent.update_ui()
            self.accept()
