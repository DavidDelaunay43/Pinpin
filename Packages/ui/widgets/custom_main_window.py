import os
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QDesktopWidget
from Packages.utils.constants.project_files import ICON_PATH, CURRENT_STYLE, STYLE_PATH, PALETTE_PATH
from Packages.utils.constants.version import VERSION
from Packages.utils.old.funcs import set_style_sheet

class CustomMainWindow(QMainWindow):
    '''
    '''
    def __init__(self, parent = None, set_style: bool = False):
        super(CustomMainWindow, self).__init__(parent)
        
        self.PARENT = parent
        
        if set_style:
            self.set_style()
    
    def init_ui(self, title = f'Pinpin - {VERSION}', icon = "pinpin_icon.ico", size = [820, 900], project = ""):
        '''
        '''
        
        self.setWindowTitle(f'{title} - {project}')
        self.resize(*size)
        self.set_icon(icon)
        self.move_main_window(self.PARENT)
        
    def set_icon(self, filename: str):
        '''
        '''
        
        icon_path = os.path.join(ICON_PATH, filename)
        self.setWindowIcon(QIcon(icon_path))
        
    def move_main_window(self, parent):
        """
        """
        
        if parent:
            parent_geometry = parent.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2 -40
            self.move(x, y)
            return
        
        desktop = QDesktopWidget()
        screen_width = desktop.screen().width()
        screen_height = desktop.screen().height()

        window_width = self.width()
        window_height = self.height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 -40

        self.move(x, y)
        
    def set_style(self):
        """
        """
        
        set_style_sheet(self, os.path.join(STYLE_PATH, CURRENT_STYLE), PALETTE_PATH)
