from PySide2.QtWidgets import QRadioButton

class CustomRadioButton(QRadioButton):
    
    def __init__(self, parent = None):
        super(CustomRadioButton, self).__init__()

        if parent:
            parent.addWidget(self)