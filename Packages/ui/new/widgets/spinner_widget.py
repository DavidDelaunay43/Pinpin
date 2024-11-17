import sys
from PySide2.QtCore import Qt, QTimer
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import QPainter, QConicalGradient

class SpinnerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(20)  # Ajuster la vitesse d'animation

    def rotate(self):
        self.angle = (self.angle + 5) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        size = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)

        gradient = QConicalGradient(0, 0, 0)
        gradient.setColorAt(0.0, Qt.transparent)
        #gradient.setColorAt(0.5, Qt.magenta)  # Couleur du rond
        gradient.setColorAt(1.0, Qt.black)

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-size / 4, -size / 4, size / 2, size / 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    spinner = SpinnerWidget()
    #spinner.resize(200, 200)
    spinner.show()

    sys.exit(app.exec_())
