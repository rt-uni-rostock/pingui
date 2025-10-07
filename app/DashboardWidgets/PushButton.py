import numpy as np
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor
from Core import *


class PushButton(QPushButton, DashboardWidget):
    def __init__(self, text, parent=None):
        QPushButton.__init__(self, text=text, parent=parent)
        self.counter = np.uint8(0)
        self.__isPressed = False
        self.__baseColor = QColor("#3d3f46")
        self.__applyStyle()

    # get memory size for input and output data
    def requiredIODatastoreSize(self):
        return (3, 1)  # input size, output size

    # serialize output data to bytes
    def packOutput(self):
        data = bytearray(1)
        data[0] = self.counter
        return data

    # deserialize input data from bytes
    def unpackInput(self, data):
        if len(data) != 3:
            return
        red = np.uint8(data[0])
        green = np.uint8(data[1])
        blue = np.uint8(data[2])
        self.__baseColor = QColor(red, green, blue)
        self.__applyStyle()
    
    # override mouse press and release events to update the button state and style
    def mousePressEvent(self, event):
        self.counter = np.uint8(self.counter + 1)
        self.__isPressed = True
        self.__applyStyle()
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.__isPressed = False
        self.__applyStyle()
        self.update()
        super().mouseReleaseEvent(event)

    def __applyStyle(self):
        if self.__isPressed:
            darkened_color = self.__baseColor.darker(120)
            self.setStyleSheet("background-color: " + darkened_color.name() + ";")
            self.__adjustTextColor()
        else:
            self.setStyleSheet("background-color: " + self.__baseColor.name() + ";")
            self.__adjustTextColor()

    def __adjustTextColor(self):
        # calculate brightness using the luminance formula
        brightness = (0.299 * self.__baseColor.red() +
                      0.587 * self.__baseColor.green() +
                      0.114 * self.__baseColor.blue())
        if brightness < 128:
            self.setStyleSheet(self.styleSheet() + "color: white;")
        else:
            self.setStyleSheet(self.styleSheet() + "color: black;")

