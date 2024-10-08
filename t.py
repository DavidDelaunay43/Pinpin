from PySide2.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QToolTip
from PySide2.QtCore import Qt, QPoint

class TableWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget Tooltip Example")

        # Création d'un QTableWidget
        self.table_widget = QTableWidget(3, 2, self)
        self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2"])

        # Ajout d'items avec des tooltips
        for row in range(3):
            for col in range(2):
                item = QTableWidgetItem(f"Item {row + 1}, {col + 1}")
                item.setToolTip(f"Tooltip for Item {row + 1}, {col + 1}")
                self.table_widget.setItem(row, col, item)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        # Connexion des signaux pour gérer les mouvements de la souris
        self.table_widget.setMouseTracking(True)
        self.table_widget.viewport().installEventFilter(self)  # Installer un filtre d'événements

    def eventFilter(self, source, event):
        if source is self.table_widget.viewport():
            if event.type() == event.ToolTip:
                # Obtenir l'item sous la souris
                item = self.table_widget.itemAt(event.pos())
                if item:
                    # Afficher le tooltip manuellement
                    QToolTip.showText(event.globalPos(), item.toolTip())
                else:
                    QToolTip.hideText()  # Cacher le tooltip si pas sur un item
            elif event.type() == event.Leave:  # Masquer le tooltip si la souris quitte la vue
                QToolTip.hideText()

        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication([])
    demo = TableWidgetDemo()
    demo.show()
    app.exec_()
