import os
from typing import Literal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QPushButton
from Packages.apps.maya_app_old.funcs.get_file import (open_maya_file, import_file, reference_file, import_file_with_file_namespace, import_file_with_custom_namespace,
                                                   reference_file_with_file_namespace, reference_file_with_user_namespace)
from Packages.utils.constants.constants_old import ICON_PATH

class MayaButton(QPushButton):
    '''
    '''
    
    def __init__(self, parent = None, mode = 'open'):
        super(MayaButton, self).__init__()
        
        parent.addWidget(self) if parent else None

        self._DICT_MODE = {
            'open': open_maya_file,
            'import no namespace': import_file,
            'import file namespace': import_file_with_file_namespace,
            'import custom namespace': import_file_with_custom_namespace,
            'reference no namespace': reference_file,
            'reference file namespace': reference_file_with_file_namespace,
            'reference custom namespace': reference_file_with_user_namespace
        }
        self.mode = 'open'
        
        self.set_mode(mode)
        self.setStyleSheet('font-size: 16px;')
        self.setMinimumHeight(40)
        
    def set_mode(self, mode: Literal['open', 'import', 'reference', 'no namespace', 'file namespace', 'custom namespace', 'import namespace', 'import custom namespace', 'import no namespace']):
        '''
        '''
        
        if not mode: return
        
        self.mode = mode
        self.setText(mode.capitalize())
        self.set_icon(mode.split(' ')[0])
        
    def set_icon(self, mode: Literal['open', 'import', 'reference']):
        '''
        '''
        
        icon_file_path = os.path.join(ICON_PATH, f'{mode}_icon.ico')
        icon = QIcon(icon_file_path)
        self.setIcon(icon)

    def get_file(self, file_path: str, custom_namespace: str = None):
        '''
        '''

        func = self._DICT_MODE[self.mode]

        if custom_namespace:
            func(file_path, custom_namespace)

        else:
            func(file_path)
