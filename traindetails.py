from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math
from db import *
from train import *
from main import *

trainslist = []

class AddTrainDialog(QtGui.QDialog):

    updateTrain = QtCore.pyqtSignal()
    def __init__(self, parent=None):

        super(AddTrainDialog,self).__init__(parent)

        self.layout = QtGui.QFormLayout(self)

        self.updateTrain.connect(lambda: MainWin().editTrainList())

        self.trainNumber = QtGui.QLineEdit()
        self.trainName = QtGui.QLineEdit()
        self.trainArrival = QtGui.QTimeEdit()

        self.trainType = QtGui.QComboBox()
        self.trainTypeList = ["Originating","Destination","Passing"]
        self.trainType.addItems(self.trainTypeList)

        self.trainToDirection = QtGui.QComboBox()
        self.trainFromDirection = QtGui.QComboBox()
        self.trainDirectionList = ["<NA>","West","East"]
        self.trainToDirection.addItems(self.trainDirectionList)
        self.trainFromDirection.addItems(self.trainDirectionList)

        self.trainType.activated[int].connect(self.trainTypeInput)
        self.trainFromDirection.activated[int].connect(self.trainFromDirectionInput)
        self.trainToDirection.activated[int].connect(self.trainToDirectionInput)


        self.buttonBox = QtGui.QDialogButtonBox()

        self.buttonOk = self.buttonBox.addButton("Add Train",QtGui.QDialogButtonBox.AcceptRole)
        self.buttonCancel = self.buttonBox.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
        self.buttonOk.clicked.connect(lambda: self.buttonClickedOk())
        self.buttonCancel.clicked.connect(lambda: self.buttonClickedCancel())
        self.buttonBox.centerButtons()

        self.layout.addRow("Train Number",self.trainNumber)
        self.layout.addRow("Train Name",self.trainName)
        self.layout.addRow("Train Type",self.trainType)
        self.layout.addRow("Arriving From",self.trainFromDirection)
        self.layout.addRow("Departing Towards",self.trainToDirection)
        self.layout.addRow("Arrival Time",self.trainArrival)
        self.layout.addRow(self.buttonBox)

    def showDialog(parent = None):

        dialog = AddTrainDialog(parent)
        result = dialog.exec_()
        return

    def trainTypeInput(self, index):
        if index==0:
            self.trainFromDirection.setEnabled(False)
            self.trainFromDirection.setCurrentIndex(0)
            self.trainToDirection.setEnabled(True)
        
        if index==1:
            self.trainToDirection.setEnabled(False)
            self.trainToDirection.setCurrentIndex(0)
            self.trainFromDirection.setEnabled(True)

        if index==2:
            self.trainFromDirection.setEnabled(True)
            self.trainToDirection.setEnabled(True)

        return

    def trainFromDirectionInput(self, index):
        if self.trainToDirection.isEnabled():
            if index==1:
                self.trainToDirection.setCurrentIndex(2)
            elif index==2:
                self.trainToDirection.setCurrentIndex(1)
        return

    def trainToDirectionInput(self, index):
        if self.trainFromDirection.isEnabled():
            if index==1:
                self.trainFromDirection.setCurrentIndex(2)
            elif index==2:
                self.trainFromDirection.setCurrentIndex(1)
        return

    def buttonClickedOk(self):

        inputTrainNumber = str(self.trainNumber.text())
        inputTrainName = str(self.trainName.text())
        inputTrainType = str(self.trainType.currentText())
        inputTrainFromDirection = str(self.trainFromDirection.currentText())
        inputTrainToDirection = str(self.trainToDirection.currentText())

        inputTime = self.trainArrival.time()
        inputHour = inputTime.hour()
        inputMinute = inputTime.minute()

        inputHourString = str(inputHour)
        if inputHour<10:
            inputHourString = "0" + inputHourString

        inputMinuteString = str(inputMinute)
        if inputMinute<10:
            inputMinuteString = "0"+inputMinuteString

        inputTimeString = inputHourString + ":" + inputMinuteString

        if inputTrainFromDirection=="<NA>":
            addTrain(inputTrainName,inputTrainNumber,inputTimeString,inputTrainToDirection,"NOT_ARRIVED",inputTrainType)
        else:
            addTrain(inputTrainName,inputTrainNumber,inputTimeString,inputTrainFromDirection,"NOT_ARRIVED",inputTrainType)
        
        temptrain = Train(1, 2, 3, 4)
        temptrain.x = 100
        temptrain.y = len(trainslist)*60 + 260
        temptrain.vel = 1
        trainslist.append(temptrain)

        QtGui.QDialog.accept(self)
        self.updateTrain.emit()

        QtGui.QApplication.processEvents()
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return

class DeleteTrainDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        super(DeleteTrainDialog,self).__init__(parent)

        self.layout = QtGui.QFormLayout(self)

        self.dropDownList = QtGui.QComboBox()
        self.trainList = []
        for train in getTrainList().find():
            self.trainList.append(train["code"])

        self.dropDownList.addItems(self.trainList)

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonOk = self.buttonBox.addButton("Delete Train",QtGui.QDialogButtonBox.AcceptRole)
        self.buttonCancel = self.buttonBox.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
        self.buttonOk.clicked.connect(lambda: self.buttonClickedOk())
        self.buttonCancel.clicked.connect(lambda: self.buttonClickedCancel())
        self.buttonBox.centerButtons()

        self.layout.addRow(self.dropDownList)
        self.layout.addRow(self.buttonBox)

    def showDialog(parent = None):

        dialog = DeleteTrainDialog(parent)
        result = dialog.exec_()
        return

    def buttonClickedOk(self):
        deleteTrain(str(self.dropDownList.currentText()))
        QtGui.QDialog.accept(self)
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return
