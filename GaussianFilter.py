# -*- coding: utf-8 -*-

from PyQt5.QtGui import QImage, qRgb, QColor
from math import pi, exp

# исходное изображение
image = QImage()
# радиус размытия
R = None
# параметр для функции Гаусса
sigma = None

def solve(radius, img):
    global image, R, sigma
    image = img
    R = radius
    sigma = (R*2 + 1) / 2 # ???
    print(changePixel(2, 2))
    return

# коэффициент матрицы Гаусса
def M(x, y):
    return 1 / (2*pi*sigma**2) * exp(-(x**2 + y**2) / 2*sigma**2)

# изменение цвета пикселя средним значением соседних пикселей
def changePixel(x, y):
    result = qRgb(255, 255, 255)
    for i in range(-R, R):
        for j in range (-R, R):
            pixel = image.pixel(x + i, y + j)
            colors = QColor(pixel).getRgb()
            print(colors)
            #result += colors*M(i, j)
            result += image.pixel(x + i, y + j)*M(i, j)
    return result
