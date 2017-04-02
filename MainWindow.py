# -*- coding: utf-8 -*-

# Сглаживание изображения с помощью масок

from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QDir, QEvent
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, 
        QLabel, QMessageBox, QInputDialog, QDialog)
import GaussianFilter
from Dialog import InputDialog

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("mainwindow.ui", self)
        
        self.lblSecondImage.setVisible(False)
        self.actionRun.triggered.connect(self.getSolve)
        self.actionRun.setShortcut('Ctrl+R')
        self.actionOpen.triggered.connect(self.openDialog)
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionSave.triggered.connect(self.saveDialog)
        self.actionSave.setShortcut('Ctrl+S')

        self.show()
    
    # выход из программы по нажатию esc
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # диалог для открытия изображения
    def openDialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", QDir.currentPath(), \
                "Images (*.png *.jpg)")
        if filename:
            self.menuTask.setEnabled(True)
            self.image = QImage(filename)
            self.resultImage = None
            if self.image.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return

            self.lblSecondImage.setVisible(False)
            self.pixmap = QPixmap.fromImage(self.image)
            # отображаем изображение, сохраняя его пропорции, не теряя качества
            self.scaledPixmap = self.pixmap.scaled(self.lblFirstImage.size(), \
                    Qt.KeepAspectRatio, \
                    Qt.SmoothTransformation)
            self.lblFirstImage.setPixmap(self.scaledPixmap)
            # событие, которое вызывается при масштабировании изображения
            self.lblFirstImage.installEventFilter(self)
            self.lblSecondImage.installEventFilter(self)
   
    # диалог для сохранения изображения, полученного после применения алгоритма
    def saveDialog(self):
        return

    # событие изменения размера изображения
    def eventFilter(self, source, event):
        # масштабируем изображение на основе нового размера компонента
        # устанавливаем разные pixmap для разных изображений
        pixmap = QPixmap()
        if (source is self.lblFirstImage):
            pixmap = self.pixmap
        elif (source is self.lblSecondImage and self.resultImage != None):
            pixmap = QPixmap.fromImage(self.resultImage)
        else:
            return super(Window, self).eventFilter(source, event)
        source.setPixmap(pixmap.scaled(source.size(), \
                Qt.KeepAspectRatio, \
                Qt.SmoothTransformation))
        return super(Window, self).eventFilter(source, event)
   
    # применение размытия по Гауссу к исходному изображению
    def getSolve(self):
        dialog = InputDialog() 
        result = dialog.exec_()
        if (result == QDialog.Accepted):
            # копируем в результат исходное изображение
            self.resultImage = QImage(self.image)
            # передаем изображение по ссылке и применяем к нему фильтр
            GaussianFilter.solve(dialog.radius, dialog.sigma, self.resultImage)
            pixmap = QPixmap.fromImage(self.resultImage)
            scaledPixmap = pixmap.scaled(self.lblSecondImage.size(), \
                    Qt.KeepAspectRatio, \
                    Qt.SmoothTransformation)
            # отображаем новое изображение на компоненте
            self.lblSecondImage.setPixmap(scaledPixmap)
            self.lblSecondImage.setVisible(True)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
