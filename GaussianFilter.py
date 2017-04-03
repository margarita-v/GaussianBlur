# -*- coding: utf-8 -*-

from PyQt5.QtGui import QImage, qRgb, QColor
from math import pi, exp, sqrt
import numpy as np

# вычисление матрицы Гаусса
def getMatrix(R, sigma):
    global matrix, horizontal, vertical
    matrix_size = 2*R + 1
    matrix = [[0 for x in range(matrix_size)] for y in range(matrix_size)]
    horizontal = [0 for x in range(matrix_size)]
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

    # вычисляем два вектора по формуле одномерного Гауссова распределения 
    total_sum = 0
    C = 1 / (sqrt(2*pi)*sigma)
    for i in range(-R, R + 1):
        horizontal[i + R] = C * exp(-(i**2) / divider)
        total_sum += horizontal[i + R]
    for i in range(-R, R + 1):
        horizontal[i + R] /= total_sum
    vertical = np.vstack(horizontal)

# применение фильтра Гаусса к изображению
def solve(R, sigma, image):
    getMatrix(R, sigma)
    for i in range(image.width()):
        for j in range(image.height()):
            changePixelColor(image, i, j, R)

# изменение цвета пикселя средним значением соседних пикселей
def changePixelColor(image, x, y, R):
    result = QColor()
    width = image.width()
    height = image.height()
    for i in range(-R, R + 1):
        for j in range (-R, R + 1):
            # берем текущий пиксель, если координаты выходят за размеры изображения
            x_current = x + i
            y_current = y + j
            if (x_current < 0 or x_current >= width):
                x_current = x
            if (y_current < 0 or y_current >= height):
                y_current = y
            # берем цвет текущего пикселя и домножаем его компоненты на элемент матрицы
            pixel = image.pixel(x_current, y_current)
            color = QColor(pixel)
            changeColor(color, matrix[i][j]) 
            addColor(result, color)
    image.setPixelColor(x, y, result)

# изменение значения цвета путем умножения его компонент на заданный коэффициент
def changeColor(color, k):
    color.setRed(color.red() * k)
    color.setGreen(color.green() * k)
    color.setBlue(color.blue() * k)

# добавление нового цвета к сумме измененных цветов
def addColor(result, secondColor):
    result.setRed(result.red() + secondColor.red())
    result.setGreen(result.green() + secondColor.green())
    result.setBlue(result.blue() + secondColor.blue())
