from PySide2.QtWidgets import QApplication, QCheckBox, QVBoxLayout, QWidget

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.checkbox = QCheckBox("Check me")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.checkbox)

        # Connexion du signal `toggled`
        self.checkbox.toggled.connect(self.on_checkbox_toggled)

        # Appel de .setChecked() avec émission manuelle du signal
        #self.checkbox.setChecked(True)  # Ne déclenche pas le signal automatiquement
        #self.checkbox.toggled.emit(True)  # Forcer le signal
        self.auto_clic()
    
    def auto_clic(self):
        self.checkbox.setChecked(True)  # Ne déclenche pas le signal automatiquement
        #self.checkbox.toggled.emit(True)  # Forcer le signal
        

    def on_checkbox_toggled(self, state):
        print(f"Checkbox toggled, state: {state}")

app = QApplication([])
window = MyWidget()
window.show()
app.exec_()
