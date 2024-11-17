import sys
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QGridLayout, QPushButton
from Packages.utils.core import Core
from Packages.utils.logger import Logger
from Packages.utils.update import Update


class UpdateDialog(QDialog):
    

    def __init__(self, parent, new_version: str):
        super(UpdateDialog, self).__init__(parent)

        self.setWindowTitle('Pinpin new release')        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._main_layout: QGridLayout = QGridLayout(self)
        self.setLayout(self._main_layout)

        self._pinpin_label: QLabel = QLabel(self)
        self._pinpin_label.setPixmap(QPixmap(str(Core.pinpin_icon_path())))
        self._update_label: QLabel = QLabel(f'New {"BETA" if "b" in new_version else ""} version {new_version} is available !')
        self._update_label.setStyleSheet('font-size: 16px')
        self._ok_button: QPushButton = QPushButton('Download', self)
        self._cancel_button: QPushButton = QPushButton('Skip', self)
        
        self._main_layout.addWidget(self._pinpin_label, 0, 0, 1, 2)
        self._main_layout.addWidget(self._update_label, 1, 0, 1, 2)
        self._main_layout.addWidget(self._ok_button, 2, 0, 1, 1)
        self._main_layout.addWidget(self._cancel_button, 2, 1, 1, 1)

        self._ok_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)


    def accept(self) -> None:
        super(UpdateDialog, self).accept()


class UpdateApp(QApplication):


    def __init__(self, argv: list[str]=sys.argv) -> None:
        super(UpdateApp, self).__init__(argv)


def main(current_version: str, parent=None) -> None:

    last_version = Update.get_last_version()
    if current_version == last_version:
        Logger.debug('You are on the latest version of Pinpin.')
        return
    
    update_dialog: UpdateDialog = UpdateDialog(parent, last_version)
    if update_dialog.exec_() == update_dialog.Accepted:
        #Logger.debug('Download latest release...')
        Update.download_installer()
        #Logger.debug('Run installer...')
        Update.run_installer()
