from PySide2.QtCore import QPoint, Qt
from PySide2.QtWidgets import QAction, QLineEdit, QMenu


class MayaLineEdit(QLineEdit):


    def __init__(self, parent):
        super(MayaLineEdit, self).__init__(parent)

        self._menu: QMenu = QMenu(self)
        self._toggle_action: QAction = QAction('Edit file name', self)
        self._toggle_action.triggered.connect(self._toggle_edition)
        self._menu.addAction(self._toggle_action)

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Activer le menu contextuel personnalisé
        self.customContextMenuRequested.connect(self._show_context_menu)  # Connecter le signal


    def _show_context_menu(self, pos: QPoint) -> None:
        self._menu.exec_(self.mapToGlobal(pos))

    
    def _toggle_edition(self) -> None:
        self.setReadOnly(not self.isReadOnly())
