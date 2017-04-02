# -*- coding: utf-8 -*-

from PyQt5.QtGui import QImage, qRgb, QColor
from math import pi, exp, sqrt

# вычисление матрицы Гаусса
def getMatrix(R, sigma):
    global matrix
    matrix_size = 2*R + 1
    matrix = [[0 for x in range(matrix_size)] for y in range(matrix_size)]
    total_sum = 0
    C = 1 / (2*pi*sigma**2)
    divider = 2*sigma**2
    # вычисляем элементы матрицы по формуле и находим сумму всех ее элементов
    for i in range(-R, R + 1):
        for j in range(-R, R + 1):
            matrix[i + R][j + R] = C * exp(-(i**2 + j**2) / divider) 
            total_sum += matrix[i + R][j + R]
    mult = 1 / total_sum
    # домножаем элементы матрицы, чтобы сумма элементов была равна 1
    for i in range(matrix_size):
        for j in range(matrix_size):
            matrix[i][j] *= mult

# применение фильтра Гаусса к изображению
def solve(R, sigma, image):
    getMatrix(R, sigma)
    for i in range (11, 100):
        for j in range (11, 100):
            #image.setPixelColor(i, j, QColor(qRgb(0, 0, 0)))
            changePixelColor(image, i, j, R)

# изменение цвета пикселя средним значением соседних пикселей
def changePixelColor(image, x, y, R):
    result = QColor()
    for i in range(-R, R + 1):
        for j in range (-R, R + 1):
            pixel = image.pixel(x + i, y + j)
            color = QColor(pixel)
            changeColor(color, matrix[i][j]) 
            addColor(result, color)
    image.setPixelColor(x, y, result)

# изменение значения цвета путем умножения его компонент на заданный коэффициент
def changeColor(color, k):
    color.setRedF(color.redF() * k)
    color.setGreenF(color.greenF() * k)
    color.setBlueF(color.blueF() * k)

# добавление нового цвета к сумме измененных цветов
def addColor(result, secondColor):
    result.setRedF(result.redF() + secondColor.redF())
    result.setGreenF(result.greenF() + secondColor.greenF())
    result.setBlueF(result.blueF() + secondColor.blueF())
