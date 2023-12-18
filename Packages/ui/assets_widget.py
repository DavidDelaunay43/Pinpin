from Packages.ui._template import PWidget
from PySide2.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout

class AssetsWt(PWidget):
    """
    """
    
    def __init__(self, parent=None) -> None:
        super(AssetsWt, self).__init__(parent)
        
        self._create_widgets()
        self._create_layout()
        
    def _create_widgets(self):
        self.asset_browser_label = QLabel("Assets")
        self.software_label = QLabel("Softwares")
        self.step_label = QLabel("Steps")
        self.file_label = QLabel("Files")
        
    def _create_layout(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        
        self.asset_browser_layout = QVBoxLayout()
        self.software_layout = QVBoxLayout()
        self.step_layout = QVBoxLayout()
        self.file_layout = QVBoxLayout()
        
        self.main_layout.addLayout(self.asset_browser_layout)
        self.main_layout.addLayout(self.software_layout)
        self.main_layout.addLayout(self.step_layout)
        self.main_layout.addLayout(self.file_layout)
        
        self.asset_browser_layout.addWidget(self.asset_browser_label)
        self.software_layout.addWidget(self.software_label)
        self.step_layout.addWidget(self.step_label)
        self.file_layout.addWidget(self.file_label)
        
        
    def _create_connections(self):
        return super()._create_connections()
        
if __name__ == '__main__':
    
    from PySide2.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    bu = AssetsWt()
    bu.show()
    app.exec_()