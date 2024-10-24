import os
from PySide2.QtWidgets import QListWidget, QWidget, QVBoxLayout, QComboBox
from Packages.logic.filefunc import get_dirs, get_publish_files

class PublishBrowser(QWidget):
    
    def __init__(self, parent = None, project_directory = None):
        super(PublishBrowser, self).__init__(parent)
        
        self._init_ui(project_directory)
        
    def _init_ui(self, project_directory):
        
        self._create_layout()
        self._create_widgets(project_directory)
        
    def _create_layout(self):
        
        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        
    def _create_widgets(self, project_directory):
        
        self._asset_box = QComboBox()
        self._publish_list = QListWidget()
        
        self._main_layout.addWidget(self._asset_box)
        self._main_layout.addWidget(self._publish_list)
        
        # Configure widgets
        asset_directory = os.path.join(project_directory, '03_asset')
        for dir in get_dirs(asset_directory):
            dir = os.path.basename(dir)
            self._asset_box.addItem(dir)
    