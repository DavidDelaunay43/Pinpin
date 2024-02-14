from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel
from Packages.apps.maya_app.ui.maya_main_window import maya_main_window
from Packages.ui.widgets import OkCancelWidget
from Packages.apps.maya_app.funcs.gpu_cache import export_gpu_cache, get_gpu_cache_file_name
from maya import cmds

class GpuCacheDialog(QDialog):
    
    def __init__(self, parent = maya_main_window()):
        super(GpuCacheDialog, self).__init__(parent)
        self.init_ui()
        self.create_widgets()
        self.create_layout()
        self.show()
        
    def init_ui(self):
        
        if not cmds.ls(selection = True):
            cmds.error('Nothing is selected.')
            
        self.setWindowTitle('Export GPU Cache')
        
    def create_widgets(self):
        self.deco_label = QLabel('Export layout as :')
        self.deco_label.setStyleSheet("font-size: 20px;")
        self.gpu_cache_name = QLabel(get_gpu_cache_file_name())
        self.gpu_cache_name.setStyleSheet("color: rgb(89, 244, 165); font-weight: bold; font-size: 20px;")

        self._ok_cancel_widget = OkCancelWidget(ok_text = 'Export GPU Cache', ok_func = self.run, cancel_func = self.close)

    def create_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.deco_label)
        self.main_layout.addWidget(self.gpu_cache_name)
        self.main_layout.addWidget(self._ok_cancel_widget)
    
    def run(self):
        export_gpu_cache()
