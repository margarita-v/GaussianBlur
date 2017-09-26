# -*- coding: utf-8 -*-

# Сглаживание изображения с помощью масок

from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QDir, QEvent
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, 
        QLabel, QMessageBox, QDialog)
from Dialog import InputDialog
from GaussianFilter import solve
from threading import Thread
import os

pictures_folder = 'pictures'
result_folder = 'result'
current_dir = QDir.currentPath()
image_filter = 'Images (*.png *.jpg)'

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("mainwindow.ui", self)
        
        self.lblSecondImage.setVisible(False)
        self.actionRun.triggered.connect(self.getSolve)
        self.actionOpen.triggered.connect(self.openDialog)
        self.actionSave.triggered.connect(self.saveDialog)
        self.actionExit.triggered.connect(self.exit)

        self.show()
    
    # диалог для открытия изображения
    def openDialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", 
                os.path.join(current_dir, pictures_folder), image_filter)
        if filename:
            self.image = QImage(filename)
            self.resultImage = None
            if self.image.isNull():
                QMessageBox.critical(self, "Image Viewer", "Cannot load %s." % fileName)
                return
            
            self.menuTask.setEnabled(True)
            self.actionRun.setEnabled(True)
            self.actionSave.setEnabled(False)

            self.lblSecondImage.setVisible(False)
            self.pixmap = QPixmap.fromImage(self.image)
            # отображаем изображение, сохраняя его пропорции, не теряя качества
            self.scaledPixmap = self.pixmap.scaled(self.lblFirstImage.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation)
            self.lblFirstImage.setPixmap(self.scaledPixmap)
            # событие, которое вызывается при масштабировании изображения
            self.lblFirstImage.installEventFilter(self)
            self.lblSecondImage.installEventFilter(self)
   
    # диалог для сохранения изображения, полученного после применения алгоритма
    def saveDialog(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save file", 
                os.path.join(current_dir, result_folder), image_filter)
        if filename:
            if not self.resultImage.save(filename):
                QMessageBox.critical(self, "Save image", 
                        "Please, enter a file extension (.jpg or .png)!")

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
        source.setPixmap(pixmap.scaled(source.size(),
                Qt.KeepAspectRatio,
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
            thread = Thread(target=solve, args=(dialog.radius, dialog.sigma, self.resultImage))
            thread.start()
            pixmap = QPixmap.fromImage(self.resultImage)
            scaledPixmap = pixmap.scaled(self.lblSecondImage.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation)
            # отображаем новое изображение на компоненте
            self.lblSecondImage.setPixmap(scaledPixmap)
            self.lblSecondImage.setVisible(True)
            self.actionSave.setEnabled(True)

    # пункт меню Exit
    def exit(self):
        result = QMessageBox.question(self, "Confirm Exit",
				  "Are you sure you want to exit ?")
        if result == QMessageBox.Yes:
            self.close()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
