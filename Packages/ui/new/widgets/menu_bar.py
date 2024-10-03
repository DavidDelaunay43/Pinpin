import os
from PySide2.QtWidgets import QAction, QMenuBar
from Packages.ui.new import widgets


class MenuBar(QMenuBar):
    
    
    def __init__(self):
        super(MenuBar, self).__init__()
        
        self._settings_action: QAction = QAction('Settings', self)
        self._help_action: QAction = QAction('Help', self)
        
        self.addAction(self._settings_action)
        self.addAction(self._help_action)
        
        self._settings_action.triggered.connect(self.open_settings_dialog)
        self._help_action.triggered.connect(self.open_documentation)
        
        self._username_corner_widget: widgets.CornerWidget = widgets.CornerWidget(text = os.getenv('USERNAME'))
        self.setCornerWidget(self._username_corner_widget)
        
        
    def open_settings_dialog(self) -> None:
        ...
        
    
    @staticmethod
    def open_documentation() -> None:
        ...
        