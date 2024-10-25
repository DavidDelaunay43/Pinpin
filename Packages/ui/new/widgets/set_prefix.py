import re
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton


class SetPrefixDialog(QDialog):


    def __init__(self, parent):
        super(SetPrefixDialog, self).__init__(parent)

        self.setWindowTitle('Set Prefix')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._main_layout: QGridLayout = QGridLayout(self)
        self.setLayout(self._main_layout)

        self._warning_label: QLabel = QLabel('WARNING !\nYou must set your project prefix as 3 capital letters.\nExample: FKP', self)
        self._warning_label.setAlignment(Qt.AlignCenter)
        self._main_layout.addWidget(self._warning_label, 0, 0, 1, 2)

        self._prefix_label: QLabel = QLabel('Project prefix:', self)
        self._main_layout.addWidget(self._prefix_label, 1, 0, 1, 1)

        self._prefix_line_edit: QLineEdit = QLineEdit(self)
        self._main_layout.addWidget(self._prefix_line_edit, 1, 1, 1, 1)

        self._run_button: QPushButton = QPushButton('Ok', self)
        self._run_button.setDefault(True)
        self._run_button.clicked.connect(self.accept)
        self._main_layout.addWidget(self._run_button, 2, 0, 1, 2)


    def accept(self):
        text: str = self._prefix_line_edit.text()
        if not text or text.isspace() or not bool(re.fullmatch(r'[A-Z]{3}', text)):
            return
        
        self.PREFIX = text
        super(SetPrefixDialog, self).accept()


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication, QMainWindow

    app: QApplication = QApplication(sys.argv)
    window: QMainWindow = QMainWindow()
    dialog: SetPrefixDialog = SetPrefixDialog(window)
    print(dialog.exec_() == dialog.Accepted)
    app.exec_()
