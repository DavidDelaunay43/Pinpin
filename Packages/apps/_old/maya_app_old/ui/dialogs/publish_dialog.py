import os
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog, QLabel, QVBoxLayout, QCheckBox, QComboBox
from Packages.apps.maya_app_old.ui.maya_main_window import maya_main_window
from Packages.apps.maya_app_old.funcs.edit_publish import publish
from Packages.apps.maya_app_old.funcs.usd import publish_usd_asset
from Packages.logic.filefunc.get_funcs import return_publish_name
from Packages.ui.widgets import OkCancelWidget
from Packages.utils.constants.constants_old import ICON_PATH
from Packages.utils.old.funcs import forward_slash
from Packages.logic.json_funcs import update_file_data, json_to_dict
from Packages.logic.filefunc.get_funcs import get_file_base_folder
from maya import cmds
from Packages.utils.constants.constants_old import VARIANTS_JSON_PATH

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

        self.setWindowTitle('Publish as')
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.variant = ''
        self._init_ui()
        self.create_connections()
        
        if cmds.ls(selection = True):
            self.exec_()
            
        else:
            cmds.error('Nothing is selected.')

    def publish_as(self):

        if self.USD:
            publish_usd_asset()
            update_file_data(forward_slash(return_publish_name(cmds.file(query = True, sceneName = True)), usd = True))
            
        else:
            publish(self.cb_delete_colon.isChecked(), self.variant)
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
        
        self.variant_label = QLabel('Variant suffix :')
        self._main_layout.addWidget(self.variant_label)
        self.variants_combo_box = QComboBox()
        self._main_layout.addWidget(self.variants_combo_box)
        variants = json_to_dict(VARIANTS_JSON_PATH)['variants']
        self.variants_combo_box.addItem('')
        for variant in variants:
            self.variants_combo_box.addItem(variant)

        self.cb_delete_colon = QCheckBox('Delete colon')
        self.cb_delete_colon.setChecked(True)
        self._main_layout.addWidget(self.cb_delete_colon)
        
        self._ok_cancel_widget = OkCancelWidget(ok_text = 'Publish as', ok_func = self.publish_as, cancel_func = self.close)
        self._main_layout.addWidget(self._ok_cancel_widget)

    def create_connections(self):
        self.variants_combo_box.currentIndexChanged.connect(self.change_variant)
        
    def change_variant(self):
        self.variant = self.sender().currentText()
        self._next_file_label.setText(f'Save as : {os.path.basename(return_publish_name(cmds.file(query = True, sceneName = True), variant = self.variant))}')
        print(self.variant)
