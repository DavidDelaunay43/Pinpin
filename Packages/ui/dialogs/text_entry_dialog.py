from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QTextEdit, QPushButton, QVBoxLayout

class TextEntryDialog(QDialog):
    def __init__(self, parent = None, text = "", title = ""):
        super().__init__(parent)
        
        self.TEXT = text
        self.TITLE = title
        self.SIZE = 200, 150
        self.init_ui()

    def init_ui(self,):
        self.setWindowTitle(self.TITLE)
        self.setMinimumSize(*self.SIZE)
        self.resize(*self.SIZE)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        # Créer un QTextEdit pour la saisie de texte
        self.text_edit = QTextEdit(self)
        self.text_edit.setText(self.TEXT)
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.End)
        self.text_edit.setTextCursor(cursor)

        # Créer un bouton "OK" pour confirmer la saisie
        self.ok_button = QPushButton("Ok", self)
        self.ok_button.setMinimumHeight(25)
        self.ok_button.clicked.connect(self.accept)

        # Créer une mise en page verticale
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_entered_text(self):
        # Renvoyer le texte saisi par l'utilisateur
        return self.text_edit.toPlainText()
