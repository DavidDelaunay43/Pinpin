from PySide2.QtWidgets import QLabel
from Packages.apps.maya_app.ui.maya_button_widget import MayaButtonWidget
from Packages.ui.base_main_window import BaseMainWindow
from Packages.apps.maya_app.ui.maya_main_window import maya_main_window
from Packages.logic.json_funcs import get_recent_files

class MayaPinpin(BaseMainWindow):
    
    def __init__(self, parent = maya_main_window()):
        super(MayaPinpin, self).__init__(parent)
        
        self.move_main_window(parent)
        
        # TEMP
        maya_tools_label = QLabel("Maya Tools")
        maya_tools_label.setStyleSheet("color: #ffffff; font-size: 16px;")
        maya_tools_label.setMinimumHeight(25)
        self.tool_layout.addWidget(maya_tools_label)
        
    def create_widgets(self):
        super().create_widgets()
        self.maya_button_widget = MayaButtonWidget()
        self.recent_maya_button_widget = MayaButtonWidget()

    def create_layout(self):
        super().create_layout()
        self._browser_file_layout.addWidget(self.maya_button_widget)
        self._recent_file_layout.addWidget(self.recent_maya_button_widget)

    def create_connections(self):
        super().create_connections()
        self.maya_button_widget.maya_button.clicked.connect(self.get_maya_file)
        self.recent_maya_button_widget.maya_button.clicked.connect(self.get_maya_file)
        
    def on_recent_tab_active(self):
        super().on_recent_tab_active()
        recent_files = get_recent_files(ext = ['.ma', '.mb', '.obj', '.fbx', '.abc'])
        self._recent_file_table.update_file_items(recent_files)
        
    def populate_list_01(self, tree_item, column):
        super().populate_list_01(tree_item, column)
        
        self._select_item_from_text(self.list_01, 'maya'.capitalize())

    def populate_list_02(self, parent_directory: str):
        super().populate_list_02(parent_directory)
        self._select_item_from_text(self.list_01, 'scenes'.capitalize())

    def get_maya_file(self):
        
        if self.maya_button_widget.maya_button.mode in ['import custom namespace', 'reference custom namespace']:
            custom_namespace = self.maya_button_widget._field_custom_namspace.text()
            self.maya_button_widget.maya_button.get_file(file_path = self.status_bar.get_text(), custom_namespace = custom_namespace)

        else:
            self.maya_button_widget.maya_button.get_file(file_path = self.status_bar.get_text())
