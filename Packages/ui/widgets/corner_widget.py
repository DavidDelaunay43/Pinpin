from PySide2.QtWidgets import QWidget, QHBoxLayout
from Packages.ui.widgets.custom_label import CustomLabel

class CornerWidget(QWidget):
    """
    """
    
    def __init__(self, parent = None, label_text: str = ''):
        super(CornerWidget, self).__init__(parent)
        
        # Create layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 10, 0)
        
        # Create label
        self.label_pixmap = CustomLabel(parent = self.main_layout)
        self.label_pixmap.setObjectName("user_icon_label")
        self.label = CustomLabel(label_text, parent = self.main_layout)
        self.label.setObjectName("user_label")
        self.label_pixmap.add_pixmap('user_icon.png')
