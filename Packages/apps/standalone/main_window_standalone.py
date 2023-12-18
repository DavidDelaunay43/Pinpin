import os
from PySide2.QtCore import Qt
from Packages.logic.json_funcs import get_dev_mode_state
from Packages.ui.base_main_window import BaseMainWindow
from Packages.ui.widgets import OpenFileWidget
from Packages.utils.logger import init_logger
from Packages.logic.json_funcs import get_recent_files

logger = init_logger(__file__)

class MainWindowStandalone(BaseMainWindow):
    """
    """
    def __init__(self, parent = None):
        super(MainWindowStandalone, self).__init__(parent, set_style = True)
        self.add_dev_mode()

    def create_widgets(self):
        super().create_widgets()
        self._open_file_widget_browser = OpenFileWidget(self.current_directory)
        self._open_file_widget_browser.setObjectName("_open_file_widget_browser")
        self._open_file_widget_recent = OpenFileWidget(None)
        self._open_file_widget_browser.setObjectName("_open_file_widget_recent")

    def create_layout(self):
        super().create_layout()
        self._browser_file_layout.addWidget(self._open_file_widget_browser)
        self._recent_file_layout.addWidget(self._open_file_widget_recent)

    def create_connections(self):
        super().create_connections()
        self._open_file_widget_browser.open_file_button.clicked.connect(self.open_file_in_app)
        self._open_file_widget_recent.open_file_button.clicked.connect(self.open_file_in_app)

    def on_browser_tab_active(self):
        super().on_browser_tab_active()
        self.status_bar.update(self.current_directory)
        print(f'current dir : {self.current_directory}')

    def on_recent_tab_active(self):
        super().on_recent_tab_active()
        self._open_file_widget_recent.update_buttons(None)
        recent_files = get_recent_files()
        self._recent_file_table.update_file_items(recent_files)
 
    def open_file_in_app(self):
        
        if self._get_active_tab_text() == 'Browser':
            self._open_file_widget_browser.open_file_in_app(self.status_bar.get_text())
            
        elif self._get_active_tab_text() == 'Recent':
            self._open_file_widget_recent.open_file_in_app(self.status_bar.get_text())

    def _on_file_item_clicked(self, item):
        super()._on_file_item_clicked(item)
        
        file_path = item.data(32)
        
        if self._get_active_tab_text() == 'Browser':
            self._open_file_widget_browser.update_buttons(file_path)
            
        elif self._get_active_tab_text() == 'Recent':
            self._open_file_widget_recent.update_buttons(file_path)
            
        else:
            return

    def _add_dir(self, item):
        super()._add_dir(item)
        self._open_file_widget_browser.update_buttons(self.status_bar.get_text())
        
    def add_dev_mode(self):

        if get_dev_mode_state():
            self._open_file_widget_browser.prefs_button.show()

        else:
            self._open_file_widget_browser.prefs_button.hide()
