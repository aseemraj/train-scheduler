import sys, random
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Platform(object):
    def __init__(self,platformNo):
        self.platformNo = platformNo
        self.occupied = False
        self.status = True
        self.trainOnPlatform = None

    def draw(self, qp):
        x = self.platformNo/2
        y = self.platformNo%2
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)
        qp.setBrush(QtGui.QColor(50, 50, 50))
        qp.drawRect(100, 230+x*60+y*15, 600, 15)