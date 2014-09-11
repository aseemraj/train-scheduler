from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math

trainwidth = 12
trainlength = 500
bogies = 20
bogielength = trainlength/bogies

class Train(object):
    """Name of the train along with his trainCode, Arrival Time Departure Time"""
    def __init__(self, code, name, departure, arrival, platform=0, status=0):
        self.code = code
        self.arrival = arrival
        self.departure = departure
        self.platform = platform
        self.vel = 0
        self.x = 0
        self.y = 0
        self.bogies = bogies
        self.tempi = 0

    def draw(self, qp):
        for i in range(self.bogies):
            if i&1:
                qp.setBrush(QtGui.QColor(200, 160, 0))
                qp.drawRect(self.x+i*bogielength, self.y, bogielength, trainwidth)
            else:
                qp.setBrush(QtGui.QColor(200, 40, 20))
                qp.drawRect(self.x+i*bogielength, self.y, bogielength, trainwidth)

    def update(self):
        """ Called each frame. """
        self.x += self.vel
        print "updating ", self.tempi
        self.tempi += 1
        if self.vel>0:
            self.bogies = int(bogies + 1 - math.ceil((self.x-200)/bogielength))
        # elif self.vel<0:
        #     self.bogies = 20 - (self.x+100)/bogielength
