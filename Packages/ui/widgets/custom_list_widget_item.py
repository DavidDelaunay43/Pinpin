from PySide2.QtWidgets import QListWidgetItem, QListWidget

class CustomListWidgetItem(QListWidgetItem):
    
    def __init__(self, text: str, listview: QListWidget):
        super(CustomListWidgetItem, self).__init__(text, listview)
        