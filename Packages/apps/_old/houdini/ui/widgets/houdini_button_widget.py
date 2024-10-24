import os
from typing import Literal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QPushButton
from Packages.apps.houdini.funcs.get_file import open_houdini_file
from Packages.utils.constants.constants_old import ICON_PATH

class HoudiniButton(QPushButton):
    '''
    '''
    
    def __init__(self, parent = None, mode = 'open'):
        super(HoudiniButton, self).__init__()
        
        parent.addWidget(self) if parent else None

        self._DICT_MODE = {
            'open': open_houdini_file,
        }
        self._MODE = 'open'
        
        self.set_mode(mode)
        self.setStyleSheet('font-size: 16px;')
        self.setMinimumHeight(40)
        
    def set_mode(self, mode: Literal['open']):
        '''
        '''
        
        if not mode: return
        
        self._MODE = mode

        if mode in ['open']:
            self.setText(mode.capitalize())
            self.set_icon(mode)
        
    def set_icon(self, mode: Literal['open']):
        '''
        '''
        
        icon_file_path = os.path.join(ICON_PATH, f'{mode}_icon.ico')
        icon = QIcon(icon_file_path)
        self.setIcon(icon)

    def get_file(self, file_path: str):
        '''
        '''

        func = self._DICT_MODE[self._MODE]

        func(file_path)
