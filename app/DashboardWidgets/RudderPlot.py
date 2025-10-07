import math
import numpy as np
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt, pyqtProperty
from PyQt5.QtWidgets import QWidget
from Core import *


class RudderPlot(QWidget, DashboardWidget):
    def __init__(self, parent=None):
        # call the constructor of the super class (QWidget)
        QWidget.__init__(self, parent=parent)

        # maximum angle range
        self.maxAngleRange = np.deg2rad(35.0)

        # set default values
        self.__commandThrottle = 0.0
        self.__commandAngle = np.deg2rad(0.0)
        self.__actualThrottle = 0.0
        self.__actualAngle = np.deg2rad(0.0)

        # default colors (can be overridden by stylesheet via qproperty-...)
        self.__cmdColor = "#0066cc"
        self.__actColor = "#00cc00"
        self.__cmdRef = "#8fadcc"
        self.__actRef = "#8fcc8f"
        self.__backgroundInner = "#f7fbfe"
        self.__backgroundOuter = "#e9eff8"
        self.__rulerDash = "#e4e6f2"
        self.__rulerSolid = "#d4d9e2"
        self.__borderColor = "#cad0d7"

    # get memory size for input and output data
    def requiredIODatastoreSize(self):
        return (16, 0)  # input size, output size

    # serialize output data to bytes
    def packOutput(self):
        return bytearray(0)  # no output data

    # deserialize input data from bytes
    def unpackInput(self, data):
        if len(data) != 16:
            return
        self.__commandAngle = np.frombuffer(data[0:4], dtype=np.float32)[0]
        self.__commandThrottle = np.frombuffer(data[4:8], dtype=np.float32)[0]
        self.__actualAngle = np.frombuffer(data[8:12], dtype=np.float32)[0]
        self.__actualThrottle = np.frombuffer(data[12:16], dtype=np.float32)[0]
        self.__commandThrottle = min(max(self.__commandThrottle, -1.0), 1.0)
        self.__actualThrottle = min(max(self.__actualThrottle, -1.0), 1.0)

    # ---------------------- Qt properties for stylesheet control ----------------------
    def getCmdColor(self):
        return self.__cmdColor

    def setCmdColor(self, value):
        if value == self.__cmdColor:
            return
        self.__cmdColor = value
        self.update()

    cmdColor = pyqtProperty(str, fget=getCmdColor, fset=setCmdColor)

    def getActColor(self):
        return self.__actColor

    def setActColor(self, value):
        if value == self.__actColor:
            return
        self.__actColor = value
        self.update()

    actColor = pyqtProperty(str, fget=getActColor, fset=setActColor)

    def getCmdRef(self):
        return self.__cmdRef

    def setCmdRef(self, value):
        if value == self.__cmdRef:
            return
        self.__cmdRef = value
        self.update()

    cmdRef = pyqtProperty(str, fget=getCmdRef, fset=setCmdRef)

    def getActRef(self):
        return self.__actRef

    def setActRef(self, value):
        if value == self.__actRef:
            return
        self.__actRef = value
        self.update()

    actRef = pyqtProperty(str, fget=getActRef, fset=setActRef)

    def getBackgroundInner(self):
        return self.__backgroundInner

    def setBackgroundInner(self, value):
        if value == self.__backgroundInner:
            return
        self.__backgroundInner = value
        self.update()

    backgroundInner = pyqtProperty(str, fget=getBackgroundInner, fset=setBackgroundInner)

    def getBackgroundOuter(self):
        return self.__backgroundOuter

    def setBackgroundOuter(self, value):
        if value == self.__backgroundOuter:
            return
        self.__backgroundOuter = value
        self.update()

    backgroundOuter = pyqtProperty(str, fget=getBackgroundOuter, fset=setBackgroundOuter)

    def getRulerDash(self):
        return self.__rulerDash

    def setRulerDash(self, value):
        if value == self.__rulerDash:
            return
        self.__rulerDash = value
        self.update()

    rulerDash = pyqtProperty(str, fget=getRulerDash, fset=setRulerDash)

    def getRulerSolid(self):
        return self.__rulerSolid

    def setRulerSolid(self, value):
        if value == self.__rulerSolid:
            return
        self.__rulerSolid = value
        self.update()

    rulerSolid = pyqtProperty(str, fget=getRulerSolid, fset=setRulerSolid)

    def getBorderColor(self):
        return self.__borderColor

    def setBorderColor(self, value):
        if value == self.__borderColor:
            return
        self.__borderColor = value
        self.update()

    borderColor = pyqtProperty(str, fget=getBorderColor, fset=setBorderColor)

    # paint event: This function is called, if the widget needs to be repainted
    def paintEvent(self, e):
        # first, we ensure, that all values are in a valid range
        self.__commandThrottle = min(max(self.__commandThrottle, -1.0), 1.0)
        self.__actualThrottle = min(max(self.__actualThrottle, -1.0), 1.0)
        self.__commandAngle = min(max(self.__commandAngle, -self.maxAngleRange), self.maxAngleRange)
        self.__actualAngle = min(max(self.__actualAngle, -self.maxAngleRange), self.maxAngleRange)

        # scale real angles to the range of visible angles (45 deg)
        angleCMD = -self.__commandAngle / self.maxAngleRange * np.deg2rad(45.0)
        angleACT = -self.__actualAngle / self.maxAngleRange * np.deg2rad(45.0)

        # relative percentage of geometrical sizes with respect to maximum radius
        percentBorder = 0.04
        percentGridBorder = 0.02
        percentLineWidthThrottle = 0.09
        percentLineWidthAngle = 0.02

        # create painter object and enable anti-aliasing
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

        # get maximum allowed radius for whole content
        maxRadius = math.floor(min(painter.device().width(), painter.device().height()) / 2.0)

        # calculate all kinds of radii and line widths and ensure that some values are multiple values of 2 or 4
        center = maxRadius
        border = math.floor(maxRadius * percentBorder)
        border = math.ceil(border / 2) * 2
        radius = maxRadius - border
        lineWidthGrid = math.floor(maxRadius * percentGridBorder)
        lineWidthThrottleCMD = math.floor(maxRadius * percentLineWidthThrottle)
        lineWidthThrottleACT = math.floor(lineWidthThrottleCMD / 2)
        lineWidthAngle = math.floor(maxRadius * percentLineWidthAngle)
        rulerMaxRadius = radius - border / 2 - lineWidthThrottleCMD

        # paint background square
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(self.__backgroundOuter), Qt.SolidPattern))
        r = radius * np.sqrt(2.0) / 2.0
        painter.drawRect(int(center-r), int(center-r), int(2*r), int(2*r))

        # paint background of two pies
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(self.__backgroundInner), Qt.SolidPattern))
        painter.drawPie(int(center-radius), int(center-radius), int(2*radius), int(2*radius), 45*16, 90*16)
        painter.drawPie(int(center-radius), int(center-radius), int(2*radius), int(2*radius), -45*16, -90*16)

        # paint ruler
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(self.__rulerDash), lineWidthGrid, Qt.DashLine, Qt.FlatCap))
        painter.drawArc(int(center-rulerMaxRadius*1.00), int(center-rulerMaxRadius*1.00), int(2*rulerMaxRadius*1.00), int(2*rulerMaxRadius*1.00), 45*16, 90*16)
        painter.drawArc(int(center-rulerMaxRadius*0.75), int(center-rulerMaxRadius*0.75), int(2*rulerMaxRadius*0.75), int(2*rulerMaxRadius*0.75), 45*16, 90*16)
        painter.drawArc(int(center-rulerMaxRadius*0.50), int(center-rulerMaxRadius*0.50), int(2*rulerMaxRadius*0.50), int(2*rulerMaxRadius*0.50), 45*16, 90*16)
        painter.drawArc(int(center-rulerMaxRadius*0.25), int(center-rulerMaxRadius*0.25), int(2*rulerMaxRadius*0.25), int(2*rulerMaxRadius*0.25), 45*16, 90*16)
        painter.drawArc(int(center-rulerMaxRadius*1.00), int(center-rulerMaxRadius*1.00), int(2*rulerMaxRadius*1.00), int(2*rulerMaxRadius*1.00), -45*16, -90*16)
        painter.drawArc(int(center-rulerMaxRadius*0.75), int(center-rulerMaxRadius*0.75), int(2*rulerMaxRadius*0.75), int(2*rulerMaxRadius*0.75), -45*16, -90*16)
        painter.drawArc(int(center-rulerMaxRadius*0.50), int(center-rulerMaxRadius*0.50), int(2*rulerMaxRadius*0.50), int(2*rulerMaxRadius*0.50), -45*16, -90*16)
        painter.drawArc(int(center-rulerMaxRadius*0.25), int(center-rulerMaxRadius*0.25), int(2*rulerMaxRadius*0.25), int(2*rulerMaxRadius*0.25), -45*16, -90*16)
        painter.setPen(QPen(QColor(self.__rulerSolid), lineWidthGrid, Qt.SolidLine, Qt.FlatCap))
        painter.drawLine(int(center), int(center-radius), int(center), int(center+radius))

        # paint reference lines for angles
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(self.__cmdRef), lineWidthAngle, Qt.DashLine, Qt.RoundCap))
        x = rulerMaxRadius * np.sin(angleCMD)
        y = rulerMaxRadius * np.cos(angleCMD)
        painter.drawLine(int(center+x), int(center-y), int(center-x), int(center+y))
        painter.setPen(QPen(QColor(self.__actRef), lineWidthAngle, Qt.DashLine, Qt.RoundCap))
        x = rulerMaxRadius * np.sin(angleACT)
        y = rulerMaxRadius * np.cos(angleACT)
        painter.drawLine(int(center+x), int(center-y), int(center-x), int(center+y))

        # paint throttle vectors
        painter.setPen(QPen(QColor(self.__cmdColor), lineWidthThrottleCMD, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(int(center), int(center), int(center + math.sin(angleCMD)*rulerMaxRadius*self.__commandThrottle), int(center - math.cos(angleCMD)*rulerMaxRadius*self.__commandThrottle))
        painter.drawPoint(int(center), int(center))
        painter.setPen(QPen(QColor(self.__actColor), lineWidthThrottleACT, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(int(center), int(center), int(center + math.sin(angleACT)*rulerMaxRadius*self.__actualThrottle), int(center - math.cos(angleACT)*rulerMaxRadius*self.__actualThrottle))
        painter.drawPoint(int(center), int(center))

        # paint a path as border around the whole widget
        path = QPainterPath()
        path.moveTo(int(center-r), int(center))
        path.lineTo(int(center-r), int(center+r))
        path.arcTo(int(center-radius), int(center-radius), int(2*radius), int(2*radius), -135, 90)
        path.lineTo(int(center+r), int(center+r))
        path.arcTo(int(center-radius), int(center-radius), int(2*radius), int(2*radius), 45, 90)
        path.closeSubpath()
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(self.__borderColor), border, Qt.SolidLine, Qt.RoundCap))
        painter.drawPath(path)
