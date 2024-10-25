from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel
from Packages.apps.maya_app.utils.ui_utils import mayaMainWindow
from Packages.utils.core import Core


class ProcsWarnindDialog(QDialog):


    def __init__(self, parent):
        super(ProcsWarnindDialog, self).__init__(parent)

        self._main_layout: QGridLayout = QGridLayout(self)
        self.setLayout(self._main_layout)

        self._warning_label: QLabel = QLabel('Warning ! Pinpin MEL procedures not found.', self)
        self._tip_label: QLabel = QLabel('Fetch Pinpin procs by clicking on the shelf button:', self)
        self._pixmap_label: QLabel = QLabel(self)

        self._pixmap_label.setPixmap(
            QPixmap(
                str(Core.pinpin_icons_path().joinpath('pimento_icon.ico')), self
            )
        )

        self._main_layout.addWidget(self._warning_label, 0, 0, 1, 2)
        self._main_layout.addWidget(self._tip_label, 1, 0, 1, 1)
        self._main_layout.addWidget(self._pixmap_label, 1, 1, 1, 1)


def main() -> None:
    dialog: ProcsWarnindDialog = ProcsWarnindDialog(mayaMainWindow)
    dialog.exec_()
