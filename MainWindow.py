# -*- coding: utf-8 -*-

# Сглаживание изображения с помощью масок

from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QDir, QEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("mainwindow.ui", self)

        self.actionOpen.triggered.connect(self.openDialog)
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionSave.triggered.connect(self.saveDialog)
        self.actionSave.setShortcut('Ctrl+S')

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def openDialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", QDir.currentPath(), \
                "Images (*.png *.jpg)")
        if filename:
            image = QImage(filename)
            self.pixmap = QPixmap(filename)
            self.scaledPixmap = self.pixmap.scaled(self.lblFirstImage.size(), \
                    Qt.KeepAspectRatio, \
                    Qt.SmoothTransformation)
            self.lblFirstImage.setPixmap(self.scaledPixmap)
            self.lblFirstImage.installEventFilter(self)            
            self.lblSecondImage.setPixmap(self.scaledPixmap)
            self.lblSecondImage.installEventFilter(self)
    
    def saveDialog(self):
        return

    def eventFilter(self, source, event):
        if ((source is self.lblFirstImage or source is self.lblSecondImage) \
                and event.type() == QEvent.Resize):
            source.setPixmap(self.pixmap.scaled(source.size(), \
                    Qt.KeepAspectRatio, \
                    Qt.SmoothTransformation))
        return super(Window, self).eventFilter(source, event)


if __name__ == '__main__':
    
    import sys
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
