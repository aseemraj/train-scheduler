import sys, random, time
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from train import *
from traindetails import *
from db import *
from platform import *
from outerline import *
from time import strftime

trains = []

class MainWin(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWin, self).__init__()
        self.initUI()
        
    def initUI(self):
        exitAction = QtGui.QAction('&Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        screen = QtGui.QDesktopWidget().screenGeometry()
        exitAction.setStatusTip('Quit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.statusBar().showMessage('Ready')
        menubar = self.menuBar()
        mainmenu = menubar.addMenu('&Control')
        mainmenu.addAction(exitAction)

        self.resize(screen.width(), screen.height())
        self.setWindowTitle('Train Traffic Simulator')
        self.center()

        # Time slider
        self.slider = QtGui.QSlider(1, self)
        self.slider.setRange(10, 100)
        self.slider.setSingleStep(10)
        self.slider.resize(500, 20)
        self.slider.move(200, 57)
 
        #Timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.Timeset())
        self.timer.start(1000)
 
        #Timer Display
        self.time = strftime("%H"+":"+"%M"+":"+"%S")
        self.timeArray = []
        self.timeArray = self.time.split(":")
        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.display(self.time)
        self.lcd.setGeometry(300,100,200,70)

        # Start button
        sbtn = QtGui.QPushButton('Start Simulation', self)
        sbtn.setToolTip('Click to start simulation')
        sbtn.resize(sbtn.sizeHint())
        sbtn.move(50, 50)
        sbtn.clicked.connect(lambda: None)
        
        # Quit button
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.setToolTip('Quit Application')
        qbtn.resize(qbtn.sizeHint())
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.move(screen.width()-200, screen.height()-120)

        #User Control Buttons
        addTrainButton = QtGui.QPushButton("Add Train", self)
        deleteTrainButton = QtGui.QPushButton("Delete Train", self)
        addPlatformButton = QtGui.QPushButton("Add Platform", self)
        editPlatformButton = QtGui.QPushButton("Edit Platform", self)
        editTrainButton = QtGui.QPushButton("Edit Train", self)

        addTrainButton.move(screen.width()-350, screen.height()-250)
        deleteTrainButton.move(screen.width()-200, screen.height()-250)
        addPlatformButton.move(screen.width()-350, screen.height()-200)
        editPlatformButton.move(screen.width()-200, screen.height()-200)
        editTrainButton.move(screen.width()-275, screen.height()-160)

        addTrainButton.clicked.connect(lambda: self.showAddTrainDialog())
        addPlatformButton.clicked.connect(lambda: self.showAddPlatformDialog())
        deleteTrainButton.clicked.connect(lambda: self.showDeleteTrainDialog())
        editPlatformButton.clicked.connect(lambda: self.showEditPlatformDialog())
        editTrainButton.clicked.connect(lambda: self.showEditTrainDialog())


        #Adding Train To Table
        view = QTableView(self)
        tableData = TrainTableModel()
        view.setModel(tableData)
        view.setGeometry(screen.width()-460,0,460,400)
 
        tableData.addTrain(TrainInfo('12480', '11:00', '11:10','4'))
        tableData.addTrain(TrainInfo('12621', '20:10', '20:30','3'))
        tableData.addTrain(TrainInfo('12480', '21:35', '21:40','6'))

        # Platform labels
        it = 0
        while it<16:
            lbl = QtGui.QLabel('PF '+str(it+1)+'/'+str(it+2), self)
            lbl.move(30, 230+it*30)
            it = it+2
        
        # self.show()

    def Timeset(self):
        print self.timeArray[2]
        self.timeArray[2] = int(self.timeArray[2]) + 10*int(self.slider.value())
        print self.timeArray[2]
        if int(self.timeArray[2]) >= 60:
            self.minute = int(self.timeArray[2])
            self.timeArray[2] = int(self.timeArray[2])%60
            self.minute = self.minute/60
            self.timeArray[1] = int(self.timeArray[1]) + self.minute
            if int(self.timeArray[1]) >= 60:
                self.hour = int(self.timeArray[1])
                self.timeArray[1] = int(self.timeArray[1])%60
                self.hour = self.hour/60
                self.timeArray[0] = int(self.timeArray[0]) + self.hour
                if int(self.timeArray[2]) >= 24:
                    self.timeArray[2] = int(self.timeArray[2])%24
        self.time = str(self.timeArray[0])+":"+str(self.timeArray[1])+":"+str(self.timeArray[2])  
        self.lcd.display(self.time)

    def showAddTrainDialog(self):
        AddTrainDialog(self).showDialog()
        return

    def showAddPlatformDialog(self):
        AddPlatformDialog(self).showDialog()
        return    

    def showDeleteTrainDialog(self):
        DeleteTrainDialog(self).showDialog()
        return

    def showEditPlatformDialog(self):
        EditPlatformDialog(self).showDialog()
        return

    def showEditTrainDialog(self):
        EditTrainDialog(self).showDialog()
        return

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPlatforms(qp)
        self.drawOuterlines(qp)
        
        for train in trains:
            train.draw(qp)
            train.update()
        self.update()
        QtGui.QApplication.processEvents()

        qp.end()
        
    def drawPlatforms(self, qp):
        Platforms = []
        for i in range(16):
            platform = Platform(i)
            platform.draw(qp)
            Platforms.append(platform)


    def drawOuterlines(self, qp):
        Outerlines = []
        for i in range(5):
            outerline = OuterLine(i)
            outerline.draw(qp)
            Outerlines.append(outerline)

        for i in range(5):
            outerline = OuterLine(i+5)
            outerline.draw(qp)
            Outerlines.append(outerline)

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Confirmation',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class AddPlatformDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        super(AddPlatformDialog,self).__init__(parent)

        self.layout = QtGui.QFormLayout(self)

        self.platformNumber = QtGui.QLineEdit()

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonOk = self.buttonBox.addButton("Add Platform(s)",QtGui.QDialogButtonBox.AcceptRole)
        self.buttonCancel = self.buttonBox.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
        self.buttonOk.clicked.connect(lambda: self.buttonClickedOk())
        self.buttonCancel.clicked.connect(lambda: self.buttonClickedCancel())
        self.buttonBox.centerButtons()

        self.layout.addRow("Number of New Platforms",self.platformNumber)
        self.layout.addRow(self.buttonBox)

    def showDialog(parent = None):

        dialog = AddPlatformDialog(parent)
        result = dialog.exec_()
        return

    def buttonClickedOk(self):
        platformCount = 0
        for platform in platforms.find():
            platformCount = platformCount + 1

        for i in range(1,int(self.platformNumber.text())+1):
            addPlatform(i+platformCount,"ENABLED","EMPTY","0")

        QtGui.QDialog.accept(self)
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return

class EditPlatformDialog(QtGui.QDialog):

    def __init__(self,parent=None):
        super(EditPlatformDialog,self).__init__(parent)

        self.layout = QtGui.QFormLayout(self)

        platformCount = 0
        for platform in platforms.find():
            platformCount = platformCount + 1

        self.platformList = []
        
        for i in range(1,platformCount+1):
            self.platformList.append(QtGui.QCheckBox("Platform "+str(i)))
            self.layout.addRow(self.platformList[i-1])

        for platform in platforms.find():
            if platform["status"]=="DISABLED":
                self.platformList[int(platform["number"])-1].setChecked(True)

        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonOk = self.buttonBox.addButton("Make Changes",QtGui.QDialogButtonBox.AcceptRole)
        self.buttonCancel = self.buttonBox.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
        self.buttonOk.clicked.connect(lambda: self.buttonClickedOk())
        self.buttonCancel.clicked.connect(lambda: self.buttonClickedCancel())
        self.buttonBox.centerButtons()

        self.layout.addRow(self.buttonBox)

    def showDialog(parent = None):

        dialog = EditPlatformDialog(parent)
        result = dialog.exec_()
        return

    def buttonClickedOk(self):
        # SOME PROBLEMS HERE!!!
        ######################
        i = 1
        for checkBox in self.platformList:
            if checkBox.isChecked():
                print i
                updatePlatformStatus(i,"DISABLED")
            else:
                updatePlatformStatus(i,"ENABLED")
            i=i+1

        QtGui.QDialog.accept(self)
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return

class EditTrainDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        super(EditTrainDialog,self).__init__(parent)

        self.layout = QtGui.QFormLayout(self)
        self.trainNumber = QtGui.QComboBox()

        
        self.trainNumberList = []
        for train in getTrainList().find():
            self.trainNumberList.append(train["code"])

        self.trainNumber.addItems(self.trainNumberList)
        self.trainNumber.setCurrentIndex(0)

        self.trainNumber.activated[int].connect(self.trainNumberSelect)

        self.trainArrival = QtGui.QTimeEdit()

        self.buttonBox = QtGui.QDialogButtonBox()

        self.buttonOk = self.buttonBox.addButton("Edit Train",QtGui.QDialogButtonBox.AcceptRole)
        self.buttonCancel = self.buttonBox.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
        self.buttonOk.clicked.connect(lambda: self.buttonClickedOk())
        self.buttonCancel.clicked.connect(lambda: self.buttonClickedCancel())
        self.buttonBox.centerButtons()

        self.layout.addRow("Train Number", self.trainNumber)
        self.layout.addRow("Arrival Time",self.trainArrival)
        self.layout.addRow(self.buttonBox)

    def showDialog(parent = None):

        dialog = EditTrainDialog(parent)
        result = dialog.exec_()
        return

    def trainNumberSelect(self,index):
        for train in getTrainList().find():
            if train["code"]==str(self.trainNumber.currentText()):
                trainTimeString = train["arrival_time"]
                splitTimeString = trainTimeString.split(':')
                timeHour = int(splitTimeString[0])
                timeMinute = int(splitTimeString[1])
                self.trainArrival.setTime(QtCore.QTime(timeHour,timeMinute))

        return

    
    def buttonClickedOk(self):

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
        print self.trainNumber
        print type(self.trainNumber)
        print str(self.trainNumber.currentText())
        print inputTimeString

        updateTrainArrivalTime(str(self.trainNumber.currentText()),inputTimeString)

        QtGui.QDialog.accept(self)
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return




def main():
    app = QtGui.QApplication(sys.argv)
    for i in range(7):
        trains.append(Train(1, 2, 3, 4))
        trains[i].x = 100
        trains[i].y = i*60 + 260
        trains[i].vel = 1

    w = MainWin()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()