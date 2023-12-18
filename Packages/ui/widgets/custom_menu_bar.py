from PySide2.QtWidgets import QMenuBar, QAction
from Packages.ui.widgets.corner_widget import CornerWidget
from Packages.ui.dialogs.option_dialog import OptionDialog
from Packages.utils.constants import USERNAME
from Packages.utils.open_documentation import open_documentation

class CustomMenuBar(QMenuBar):
    
    def __init__(self,mainwindow):
        super(CustomMenuBar, self).__init__()
        self.settings_action = QAction('Settings', self)
        self.help_action = QAction('Help', self)
        self.settings_action.triggered.connect(self.open_option_window)
        self.help_action.triggered.connect(open_documentation)
        
        self.addAction(self.settings_action)
        self.addAction(self.help_action)
        
        # Display username
        self.corner_widget = CornerWidget(label_text = USERNAME)
        self.setCornerWidget(self.corner_widget)

    
    def open_option_window(self):
        self.option_window_app = OptionDialog(self).exec_()
        
