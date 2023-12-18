import hou
from Packages.ui.base_main_window import BaseMainWindow
from Packages.apps.houdini.ui.widgets.houdini_button_widget import HoudiniButton
from Packages.logic.json_funcs import get_recent_files

class HoudiniPinpin(BaseMainWindow):
    
    def __init__(self, parent = hou.ui.mainQtWindow()):
        super(HoudiniPinpin, self).__init__(parent)
        
        self.move_main_window(parent=parent)
        
    def create_widgets(self):
        super().create_widgets()
        self.houdini_button_widget = HoudiniButton()
        self.recent_houdini_button_widget = HoudiniButton()
        
    def create_layout(self):
        super().create_layout()
        self._browser_file_layout.addWidget(self.houdini_button_widget)
        self._recent_file_layout.addWidget(self.recent_houdini_button_widget)
        
    def on_recent_tab_active(self):
        super().on_recent_tab_active()
        recent_files = get_recent_files(ext = ['.hip', '.hipnc'])
        self._recent_file_table.update_file_items(recent_files)
        
    def populate_list_01(self, tree_item, column):
        super().populate_list_01(tree_item, column)
        
        self._select_item_from_text(self.list_01, 'houdini'.capitalize()) #
        
    def create_connections(self):
        super().create_connections()
        
        self.houdini_button_widget.clicked.connect(self.get_houdini_file)
        
    def get_houdini_file(self):
        '''
        '''
        
        self.houdini_button_widget.get_file(file_path = self.status_bar.get_text())
