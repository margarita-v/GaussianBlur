# -*- coding: utf-8 -*-

from PyQt5.QtGui import QImage, qRgb, QColor
from math import pi, exp, sqrt

def solve(R, image):
    for i in range (11, 15):
        for j in range (11, 15):
            #image.setPixelColor(i, j, QColor(qRgb(0, 0, 0)))
            changePixelColor(image, i, j, R)
    return image

# элемент матрицы Гаусса
def M(x, y, R, C):
    return C * exp(-(x**2 + y**2) / (2*R**2))

# изменение цвета пикселя средним значением соседних пикселей
def changePixelColor(image, x, y, R):
    result = QColor()
    # коэффициент для матрицы Гаусса
    C = 1 / (2*pi*R**2)
    s = 0
    for i in range(-R, R + 1):
        for j in range (-R, R + 1):
            s += M(i, j, R, C)
    print(1 / s)

    for i in range(-R, R + 1):
        for j in range (-R, R + 1):
            pixel = image.pixel(x + i, y + j)
            color = QColor(pixel)
            changeColor(color, M(i, j, R, C))
            addColor(result, color)

    #print(image.pixelColor(x, y).getRgb())        
    image.setPixelColor(x, y, result)
    #print(image.pixelColor(x, y).getRgb())        

# изменение значения цвета путем умножения его компонент на заданный коэффициент
def changeColor(color, k):
    color.setRedF(color.redF() * k)
    color.setGreenF(color.greenF() * k)
    color.setBlueF(color.blueF() * k)

# добавление нового цвета к сумме измененных цветов
def addColor(result, secondColor):
    result.setRed(result.red() + secondColor.red())
    result.setGreen(result.green() + secondColor.green())
    result.setBlue(result.blue() + secondColor.blue())
