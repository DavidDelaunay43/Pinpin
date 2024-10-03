from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget
from Packages.ui.new import widgets
from Packages.utils.core import Core


class CornerWidget(QWidget):
    
    
    def __init__(self, parent = None, text: str = ''):
        super(CornerWidget, self).__init__(parent)
        
        self._main_layout = QHBoxLayout()
        self.setLayout(self._main_layout)
        self._main_layout.setContentsMargins(0,0,10,0)
        
        self._pixmap_label: widgets.PixmapLabel = widgets.PixmapLabel(
            icon_path = Core.pinpin_icons_path().joinpath(Core.USER_ICON_NAME)
        )
        self._label: QLabel = QLabel(text)
