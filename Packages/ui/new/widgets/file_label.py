
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QLabel


class FileLabel(QLabel):


    def __init__(self, parent):
        super(FileLabel, self).__init__(parent)

        self.setObjectName('file_label')

        font: QFont = QFont()
        font.setPointSize(12)
        self.setFont(font)
