import os
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QLabel, QVBoxLayout
from Packages.logic.filefunc import return_increment_edit
from Packages.apps.maya_app.ui.maya_main_window import maya_main_window
from Packages.apps.maya_app.funcs import increment_edit
from Packages.ui.widgets import OkCancelWidget
from Packages.utils.funcs import forward_slash
from Packages.logic.json_funcs import update_file_data
from maya import cmds

class EditDialog(QDialog):

    def __init__(self, parent = maya_main_window(), file_path = cmds.file(query = True, sceneName = True)) -> None:
        super().__init__(parent)

        self._CURRENT_FILE_PATH = file_path
        self._CURRENT_FILE = os.path.basename(file_path)

        self._NEXT_FILE_PATH = return_increment_edit(file_path)
        self._NEXT_FILE = os.path.basename(self._NEXT_FILE_PATH)

        self.setWindowTitle('Save as')
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self._init_ui()
        
        self.exec_()

    def save_as(self):

        increment_edit()
        update_file_data(forward_slash(cmds.file(query = True, sceneName = True)))
        update_file_data(forward_slash(self._NEXT_FILE_PATH ))
        self.close()

    def _init_ui(self):

        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)

        self._current_file_label = QLabel(f'Current file : {os.path.basename(cmds.file(query = True, sceneName = True))}')
        self._main_layout.addWidget(self._current_file_label)
        self._current_file_label.setStyleSheet("font-size: 20px;")

        self._next_file_label = QLabel(f'Save as : {self._NEXT_FILE}')
        self._main_layout.addWidget(self._next_file_label)
        self._next_file_label.setStyleSheet("color: rgb(128, 255, 141); font-weight: bold; font-size: 20px;")

        self._ok_cancel_widget = OkCancelWidget(ok_text = 'Save as', ok_func = self.save_as, cancel_func = self.close)
        self._main_layout.addWidget(self._ok_cancel_widget)
