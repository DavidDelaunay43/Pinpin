from PySide2.QtWidgets import QLabel
from Packages.utils.old.funcs import forward_slash

class StatusBar(QLabel):
    """
    """
    
    def __init__(self, text='', parent = None):
        super(StatusBar, self).__init__(text)
        
        if parent:
            parent.addWidget(self)
            
        self.setStyleSheet("font-weight: bold;")
        self.setStyleSheet("font-size: 12px;")
            
    def get_text(self): 
        return self.text()
        
    def update(self, string: str):
        """
        """
        
        string = forward_slash(string)
        self.setText(string)
        
    def return_files(self):
        """
        """
        
        path = self.get_text()
 