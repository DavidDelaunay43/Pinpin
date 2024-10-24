import os
from PySide2.QtWidgets import QAction, QMenuBar
from Packages.ui.new.widgets import CornerWidget
from Packages.utils.core import Core
from Packages.utils.open_documentation import Doc


class MenuBar(QMenuBar):
    
    
    def __init__(self, parent = None):
        super(MenuBar, self).__init__(parent)
        
        self.menu = self.addMenu('Documentation')

        self._rtddoc_action: QAction = QAction('ReadTheDocs', self)
        self._ggdoc_action: QAction = QAction('GoogleDocs', self)
        self._videodoc_action: QAction = QAction('Video', self)
        
        self.menu.addAction(self._rtddoc_action)
        self.menu.addAction(self._ggdoc_action)
        self.menu.addAction(self._videodoc_action)
        
        self._rtddoc_action.triggered.connect(Doc.open_rtd_doc)
        self._ggdoc_action.triggered.connect(Doc.open_ggd_doc)
        self._videodoc_action.triggered.connect(Doc.open_video_doc)
        
        self.username_widget: CornerWidget = CornerWidget(text = Core.username())
        self.setCornerWidget(self.username_widget)
