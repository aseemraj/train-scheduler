import sys, random
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class OuterLine(object):
    def __init__(self,lineNo):
        self.lineNo = lineNo
        self.occupied = False
        self.status = True
        self.trainOnLine = None

    def draw(self, qp):
        if self.lineNo < 5:
            x = 50
        else:
            x = 550
        y = self.lineNo%5
        color = QtGui.QColor(0, 100, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)
        qp.setBrush(QtGui.QColor(50, 100, 50))
        qp.drawRect(x, 130+y*10, 200, 5)
        qp.setBrush(QtGui.QColor(20, 20, 20))