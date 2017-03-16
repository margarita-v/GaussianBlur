# -*- coding: utf-8 -*-

# Сглаживание изображения с помощью масок

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("mainwndow.ui", self)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
