# -*- coding: utf-8 -*-

from PyQt5.QtGui import QImage, qRgb, QColor
from math import pi, exp, sqrt

# вычисление матрицы Гаусса
def getMatrix(R):
    global matrix
    matrix = [[0 for x in range(2*R + 1)] for y in range(2*R + 1)]
    total_sum = 0
    kernel_R = R # // 2
    C = 1 / (2*pi*R**2)
    # вычисляем элементы матрицы по формуле и находим сумму всех ее элементов
    for i in range(-kernel_R, kernel_R + 1):
        for j in range(-kernel_R, kernel_R + 1):
            matrix[i + kernel_R][j + kernel_R] = C * exp(-(i**2 + j**2) / (2*R**2))
            total_sum += matrix[i + kernel_R][j + kernel_R]
    mult = 1 / total_sum
    # домножаем элементы матрицы, чтобы сумма элементов была равна 1
    for i in range(R):
        for j in range(R):
            matrix[i][j] *= mult
            print(matrix[i][j])
        print()

def solve(R, image):
    getMatrix(R)
    for i in range (11, 20):
        for j in range (11, 20):
            #image.setPixelColor(i, j, QColor(qRgb(0, 0, 0)))
            changePixelColor(image, i, j, R)
    return image

# изменение цвета пикселя средним значением соседних пикселей
def changePixelColor(image, x, y, R):
    result = QColor()

    for i in range(-R, R + 1):
        for j in range (-R, R + 1):
            pixel = image.pixel(x + i, y + j)
            color = QColor(pixel)
            changeColor(color, matrix[i][j]) 
            addColor(result, color)

    print(image.pixelColor(x, y).getRgb())        
    image.setPixelColor(x, y, result)
    print(image.pixelColor(x, y).getRgb())        

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
