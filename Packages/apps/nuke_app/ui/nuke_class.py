from PySide2.QtCore import Qt
from Packages.ui.base_main_window import BaseMainWindow

class NukePinpin(BaseMainWindow):
    
    def __init__(self):
        super(NukePinpin, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        