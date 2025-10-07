import math
import numpy as np
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, pyqtProperty
from PyQt5.QtWidgets import QWidget
from Core import *


class VectorPlot(QWidget, DashboardWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # set default values
        self.__commandRadius = 0.0
        self.__commandAngle = 0.0
        self.__commandZ = 0.0
        self.__actualRadius = 0.0
        self.__actualAngle = 0.0
        self.__actualZ = 0.0

        # default colors (can be overridden via qproperty-<name> in stylesheets)
        self.__cmdColor = "#0066cc"
        self.__actColor = "#00cc00"
        self.__backgroundInner = "#f7fbfe"
        self.__backgroundRing = "#e9eff8"
        self.__rulerOuter = "#fff"
        self.__rulerInnerDash = "#e4e6f2"
        self.__rulerInnerSolid = "#d4d9e2"
        self.__borderColor = "#cad0d7"

    # get memory size for input and output data
    def requiredIODatastoreSize(self):
        return (24, 0)  # input size, output size

    # serialize output data to bytes
    def packOutput(self):
        return bytearray(0)  # no output data

    # deserialize input data from bytes
    def unpackInput(self, data):
        if len(data) != 24:
            return
        self.__commandRadius = np.frombuffer(data[0:4], dtype=np.float32)[0]
        self.__commandAngle = np.frombuffer(data[4:8], dtype=np.float32)[0]
        self.__commandZ = np.frombuffer(data[8:12], dtype=np.float32)[0]
        self.__actualRadius = np.frombuffer(data[12:16], dtype=np.float32)[0]
        self.__actualAngle = np.frombuffer(data[16:20], dtype=np.float32)[0]
        self.__actualZ = np.frombuffer(data[20:24], dtype=np.float32)[0]
        self.__commandRadius = min(max(self.__commandRadius, 0.0), 1.0)
        self.__commandZ = min(max(self.__commandZ, -1.0), 1.0)
        self.__actualRadius = min(max(self.__actualRadius, 0.0), 1.0)
        self.__actualZ = min(max(self.__actualZ, -1.0), 1.0)


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

    def getBackgroundInner(self):
        return self.__backgroundInner

    def setBackgroundInner(self, value):
        if value == self.__backgroundInner:
            return
        self.__backgroundInner = value
        self.update()

    backgroundInner = pyqtProperty(str, fget=getBackgroundInner, fset=setBackgroundInner)

    def getBackgroundRing(self):
        return self.__backgroundRing

    def setBackgroundRing(self, value):
        if value == self.__backgroundRing:
            return
        self.__backgroundRing = value
        self.update()

    backgroundRing = pyqtProperty(str, fget=getBackgroundRing, fset=setBackgroundRing)

    def getRulerOuter(self):
        return self.__rulerOuter

    def setRulerOuter(self, value):
        if value == self.__rulerOuter:
            return
        self.__rulerOuter = value
        self.update()

    rulerOuter = pyqtProperty(str, fget=getRulerOuter, fset=setRulerOuter)

    def getRulerInnerDash(self):
        return self.__rulerInnerDash

    def setRulerInnerDash(self, value):
        if value == self.__rulerInnerDash:
            return
        self.__rulerInnerDash = value
        self.update()

    rulerInnerDash = pyqtProperty(str, fget=getRulerInnerDash, fset=setRulerInnerDash)

    def getRulerInnerSolid(self):
        return self.__rulerInnerSolid

    def setRulerInnerSolid(self, value):
        if value == self.__rulerInnerSolid:
            return
        self.__rulerInnerSolid = value
        self.update()

    rulerInnerSolid = pyqtProperty(str, fget=getRulerInnerSolid, fset=setRulerInnerSolid)

    def getBorderColor(self):
        return self.__borderColor

    def setBorderColor(self, value):
        if value == self.__borderColor:
            return
        self.__borderColor = value
        self.update()

    borderColor = pyqtProperty(str, fget=getBorderColor, fset=setBorderColor)

    # paint Event: this function is called, if the widget is to be painted
    def paintEvent(self, e):
        # first, we ensure, that all values are in a valid range
        self.__commandRadius = min(max(self.__commandRadius, 0.0), 1.0)
        self.__commandZ = min(max(self.__commandZ, -1.0), 1.0)
        self.__actualRadius = min(max(self.__actualRadius, 0.0), 1.0)
        self.__actualZ = min(max(self.__actualZ, -1.0), 1.0)

        # relative percentage of geometrical sizes with respect to maximum radius
        percentOuterBorder = 0.015
        percentInnerBorder = 0.012
        percentRing = 0.14
        percentGridBorder = 0.01
        percentLineWidthThrust = 0.07

        # create painter object and enable anti-aliasing
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

        # get maximum allowed radius for whole content
        maxRadius = math.floor(min(painter.device().width(), painter.device().height()) / 2.0)

        # calculate all kinds of radii and line widths and ensure that some values are multiple values of 2 or 4
        center = maxRadius
        outerBorder = math.floor(maxRadius * percentOuterBorder)
        outerBorder = math.ceil(outerBorder / 2) * 2
        outerRadius = maxRadius - outerBorder
        ringDimension = math.floor(maxRadius * percentRing)
        ringDimension = math.ceil(ringDimension / 4) * 4
        innerBorder = math.floor(maxRadius * percentInnerBorder)
        innerBorder = math.ceil(innerBorder / 2) * 2
        innerRadius = outerRadius - ringDimension
        lineWidthGrid = math.floor(maxRadius * percentGridBorder)
        lineWidthThrustCMD = math.floor(maxRadius * percentLineWidthThrust)
        lineWidthThrustACT = math.floor(lineWidthThrustCMD / 2)
        rulerMaxRadius = innerRadius - innerBorder / 2 - lineWidthThrustCMD

        # paint outer circle with ruler
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(self.__backgroundRing), Qt.SolidPattern))
        painter.drawEllipse(int(center-outerRadius), int(center-outerRadius), int(2*outerRadius), int(2*outerRadius))
        painter.setPen(QPen(QColor(self.__rulerOuter), lineWidthGrid, Qt.SolidLine, Qt.FlatCap))
        painter.drawLine(int(center - (outerRadius - outerBorder/2)), int(center), int(center + (outerRadius - outerBorder/2)), int(center))
        painter.drawLine(int(center), int(center - (outerRadius - outerBorder/2)), int(center), int(center + (outerRadius - outerBorder/2)))
        painter.drawLine(int(center - (outerRadius - outerBorder/2)/math.sqrt(2)), int(center - (outerRadius - outerBorder/2)/math.sqrt(2)), int(center + (outerRadius - outerBorder/2)/math.sqrt(2)), int(center + (outerRadius - outerBorder/2)/math.sqrt(2)))
        painter.drawLine(int(center - (outerRadius - outerBorder/2)/math.sqrt(2)), int(center + (outerRadius - outerBorder/2)/math.sqrt(2)), int(center + (outerRadius - outerBorder/2)/math.sqrt(2)), int(center - (outerRadius - outerBorder/2)/math.sqrt(2)))

        # paint inner circle with ruler
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(self.__backgroundInner), Qt.SolidPattern))
        painter.drawEllipse(int(center-innerRadius), int(center-innerRadius), int(2*innerRadius), int(2*innerRadius))
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(self.__rulerInnerDash), lineWidthGrid, Qt.DashLine, Qt.RoundCap))
        painter.drawEllipse(int(center-rulerMaxRadius*1.00), int(center-rulerMaxRadius*1.00), int(2*rulerMaxRadius*1.00), int(2*rulerMaxRadius*1.00))
        painter.drawEllipse(int(center-rulerMaxRadius*0.75), int(center-rulerMaxRadius*0.75), int(2*rulerMaxRadius*0.75), int(2*rulerMaxRadius*0.75))
        painter.drawEllipse(int(center-rulerMaxRadius*0.50), int(center-rulerMaxRadius*0.50), int(2*rulerMaxRadius*0.50), int(2*rulerMaxRadius*0.50))
        painter.drawEllipse(int(center-rulerMaxRadius*0.25), int(center-rulerMaxRadius*0.25), int(2*rulerMaxRadius*0.25), int(2*rulerMaxRadius*0.25))
        painter.setPen(QPen(QColor(self.__rulerInnerSolid), lineWidthGrid, Qt.SolidLine, Qt.FlatCap))
        painter.drawLine(int(center - innerRadius), int(center), int(center + innerRadius), int(center))
        painter.drawLine(int(center), int(center - innerRadius), int(center), int(center + innerRadius))

        # paint throttle vector (X,Y)
        painter.setPen(QPen(QColor(self.__cmdColor), lineWidthThrustCMD, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(int(center), int(center), int(center + math.sin(self.__commandAngle)*rulerMaxRadius*self.__commandRadius), int(center - math.cos(self.__commandAngle)*rulerMaxRadius*self.__commandRadius))
        painter.drawPoint(int(center), int(center))
        painter.setPen(QPen(QColor(self.__actColor), lineWidthThrustACT, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(int(center), int(center), int(center + math.sin(self.__actualAngle)*rulerMaxRadius*self.__actualRadius), int(center - math.cos(self.__actualAngle)*rulerMaxRadius*self.__actualRadius))
        painter.drawPoint(int(center), int(center))

        # paint z throttle
        painter.setPen(QPen(QColor(self.__cmdColor), ringDimension/2, Qt.SolidLine, Qt.FlatCap))
        painter.drawArc(int(center - outerRadius + ringDimension/4), int(center - outerRadius + ringDimension/4), int(2*(innerRadius + 0.75*ringDimension)), int(2*(innerRadius + 0.75*ringDimension)), int(90*16), int(-180*16*self.__commandZ))
        painter.setPen(QPen(QColor(self.__actColor), ringDimension/2, Qt.SolidLine, Qt.FlatCap))
        painter.drawArc(int(center - innerRadius - ringDimension/4), int(center - innerRadius - ringDimension/4), int(2*(innerRadius + 0.25*ringDimension)), int(2*(innerRadius + 0.25*ringDimension)), int(90*16), int(-180*16*self.__actualZ))

        # borders (inner and outer circle)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(self.__borderColor), innerBorder, Qt.SolidLine))
        painter.drawLine(int(center), int(center - (outerRadius - outerBorder/2)), int(center), int(center - innerRadius))
        painter.drawEllipse(int(center-innerRadius), int(center-innerRadius), int(2*innerRadius), int(2*innerRadius))
        painter.setPen(QPen(QColor(self.__borderColor), outerBorder, Qt.SolidLine))
        painter.drawEllipse(int(center-outerRadius), int(center-outerRadius), int(2*outerRadius), int(2*outerRadius))
