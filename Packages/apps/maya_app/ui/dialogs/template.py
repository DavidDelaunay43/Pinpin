from PySide2.QtWidgets import QDialog
from Packages.apps.maya_app.ui.maya_main_window import maya_main_window

class TemplateDialog(QDialog):
    
    def __init__(self, parent = maya_main_window()):
        super(TemplateDialog, self).__init__(parent)
        self.init_ui()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.show()
        
    def init_ui(self):
        self.setWindowTitle('')
        
    def create_widgets(self):
        pass
    
    def create_layout(self):
        pass
        
    def create_connections(self):
        pass
    
    def run(self):
        pass
