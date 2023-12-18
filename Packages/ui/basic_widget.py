from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout

class BasicWidget(QWidget):
    """
    """
    
    def __init__(self, parent = None):
        super(BasicWidget, self).__init__(parent)
        
        self._create_widgets()
        self._create_layout()
        
    def _create_widgets(self):
        self.button = QPushButton("Pimento")
        
    def _create_layout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.main_layout.addWidget(self.button)

if __name__ == '__main__':
    
    from PySide2.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    bu = BasicWidget()
    bu.show()
    app.exec_()