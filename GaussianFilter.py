# -*- coding: utf-8 -*-

from PyQt5.QtGui import QImage, qRgb, QColor
from math import pi, exp, sqrt
from threading import Thread

# Модуль для размытия по Гауссу
# Используется сепарабельность Гауссова размытия

# вычисляем вектор по формуле одномерного Гауссова распределения 
def getVector(R, sigma):
    global vector
    matrix_size = 2*R + 1
    vector = [0 for x in range(matrix_size)]

    total_sum = 0
    divider = 2*sigma**2
    C = 1 / (sqrt(2*pi)*sigma)
    for i in range(-R, R + 1):
        vector[i + R] = C * exp(-(i**2) / divider)
        total_sum += vector[i + R]
    # нормализуем значения вектора
    for i in range(-R, R + 1):
        vector[i + R] /= total_sum

# применение фильтра Гаусса к изображению
def solve(R, sigma, image):
    thread = Thread(target=getVector, args=(R, sigma))
    thread.start()
    width = image.width()
    height = image.height()
    # первый проход - горизонтальное размытие
    t1 = Thread(target=horizontal, args=(width, height, image, R))
    t1.start()
    t1.join()
    #for j in range(height):
     #   for i in range(width):
      #      t1 = Thread(target=changePixelColor, args=(image, i, j, True, R))
       #     t1.start()
    # второй проход - вертикальное размытие
    t2 = Thread(target=vertical, args=(width, height, image, R))
    t2.start()
    #for i in range(width):
     #   for j in range(height):
      #      t2 = Thread(target=changePixelColor, args=(image, i, j, False, R))
       #     t2.start()

def horizontal(width, height, image, R):
    for j in range(height):
        for i in range(width):
            changePixelColor(image, i, j, True, R)


def vertical(width, height, image, R):
    for i in range(width):
        for j in range(height):
            changePixelColor(image, i, j, False, R)

# изменение цвета пикселя средним значением соседних пикселей
# isHorizontal = True, если мы движемся по горизонтали, иначе False
def changePixelColor(image, x, y, isHorizontal, R):
    result = QColor()
    for i in range(-R, R + 1):
        x_current = x + i
        y_current = y + i
        # проверяем правильность координат в зависимости от направления движения
        if isHorizontal:
            # при движении по горизонтали y не меняется
            y_current = y
            if (x_current < 0 or x_current >= image.width()):
                x_current = x
        else:
            # при движении по вертикали x не меняется
            x_current = x
            if (y_current < 0 or y_current >= image.height()):
                y_current = y
        # берем цвет текущего пикселя и домножаем его компоненты на элемент вектора
        pixel = image.pixel(x_current, y_current)
        color = QColor(pixel)
        changeColor(color, vector[i + R])
        addColor(result, color)
    # сохраняем полученный цвет в изображение
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
