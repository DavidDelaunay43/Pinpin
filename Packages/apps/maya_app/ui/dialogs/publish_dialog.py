import os
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog, QLabel, QVBoxLayout, QCheckBox
from Packages.apps.maya_app.ui.maya_main_window import maya_main_window
from Packages.apps.maya_app.funcs.edit_publish import publish
from Packages.apps.maya_app.funcs.usd import publish_usd_asset
from Packages.logic.filefunc.get_funcs import return_publish_name
from Packages.ui.widgets import OkCancelWidget
from Packages.utils.constants import ICON_PATH
from Packages.utils.funcs import forward_slash
from Packages.logic.json_funcs import update_file_data
from maya import cmds

class PublishDialog(QDialog):

    def __init__(self, parent = maya_main_window(), file_path = cmds.file(query = True, sceneName = True), usd: bool = False) -> None:
        super(PublishDialog, self).__init__(parent)
        
        self.USD = usd
        if self.USD:
            self.setWindowIcon(QIcon(os.path.join(ICON_PATH, 'usd_icon.ico')))

        self._CURRENT_FILE_PATH = file_path
        self._CURRENT_FILE = os.path.basename(file_path)

        self._NEXT_FILE_PATH = return_publish_name(self._CURRENT_FILE, usd = self.USD)
        self._NEXT_FILE = os.path.basename(self._NEXT_FILE_PATH)

        self.setWindowTitle('Save as')
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self._init_ui()
        
        if cmds.ls(selection = True):
            self.exec_()
            
        else:
            cmds.error('Nothing is selected.')

    def publish_as(self):

        if self.USD:
            publish_usd_asset()
            update_file_data(forward_slash(return_publish_name(cmds.file(query = True, sceneName = True)), usd = True))
            
        else:
            publish(self.cb_delete_colon.isChecked())
            update_file_data(forward_slash(return_publish_name(cmds.file(query = True, sceneName = True))))

        update_file_data(forward_slash(cmds.file(query = True, sceneName = True)))
        self.close()

    def _init_ui(self):

        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)

        self._current_file_label = QLabel(f'Current file : {os.path.basename(cmds.file(query = True, sceneName = True))}')
        self._main_layout.addWidget(self._current_file_label)
        self._current_file_label.setStyleSheet("font-size: 20px;")

        self._next_file_label = QLabel(f'Save as : {os.path.basename(return_publish_name(cmds.file(query = True, sceneName = True)))}')
        self._main_layout.addWidget(self._next_file_label)
        self._next_file_label.setStyleSheet("color: rgb(128, 192, 255); font-weight: bold; font-size: 20px;")

        self._ok_cancel_widget = OkCancelWidget(ok_text = 'Publish as', ok_func = self.publish_as, cancel_func = self.close)
        self._main_layout.addWidget(self._ok_cancel_widget)

        self.cb_delete_colon = QCheckBox('Delete colon')
        self.cb_delete_colon.setChecked(True)
        self._main_layout.addWidget(self.cb_delete_colon)
