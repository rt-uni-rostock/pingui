import numpy as np
from PyQt5.QtWidgets import QLineEdit, QSizePolicy
from PyQt5.QtGui import QColor
from Core import *
from PyQt5.QtGui import QMouseEvent


class NumericDisplayFloat32(QLineEdit, DashboardWidget):
    def __init__(self, num_digits=4, parent=None):
        QLineEdit.__init__(self, parent=parent)
        self.setReadOnly(True)
        self.mousePressEvent = self.disable_mouse_event
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.__numDigits = num_digits
        self.__backgroundColor = QColor("#FFFFFF")
        self.__foregroundColor = QColor("#000000")
        self.__applyStyle()

    # get memory size for input and output data
    def requiredIODatastoreSize(self):
        return (10, 0)  # input size, output size

    # serialize output data to bytes
    def packOutput(self):
        return bytearray(0)  # no output data

    # deserialize input data from bytes
    def unpackInput(self, data):
        if len(data) != 10:
            return
        value = np.frombuffer(data[0:4], dtype=np.float32)[0]
        f_red = np.uint8(data[4])
        f_green = np.uint8(data[5])
        f_blue = np.uint8(data[6])
        b_red = np.uint8(data[7])
        b_green = np.uint8(data[8])
        b_blue = np.uint8(data[9])
        self.__foregroundColor = QColor(f_red, f_green, f_blue)
        self.__backgroundColor = QColor(b_red, b_green, b_blue)
        self.setText(str(round(value, self.__numDigits)))
        self.__applyStyle()

    def disable_mouse_event(self, event: QMouseEvent):
        pass

    def __applyStyle(self):
        self.setStyleSheet("color: " + self.__foregroundColor.name() + "; background-color: " + self.__backgroundColor.name() + ";")

