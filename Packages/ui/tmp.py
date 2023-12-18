from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class ConfirmationDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Confirmation")
        
        layout = QVBoxLayout()
        
        label = QLabel(message)
        layout.addWidget(label)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)  # Accepter le dialogue lorsque OK est cliqué
        layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.reject)  # Rejeter le dialogue lorsque Annuler est cliqué
        layout.addWidget(cancel_button)
        
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = ConfirmationDialog("Voulez-vous effectuer cette action ?")
    
    result = dialog.exec_()
    if result == QDialog.Accepted:
        print("L'utilisateur a cliqué sur OK")
    else:
        print("L'utilisateur a cliqué sur Annuler ou a fermé la fenêtre")

    sys.exit(app.exec_())
