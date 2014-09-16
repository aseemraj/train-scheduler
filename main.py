import sys, random
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from platform import *
from outerline import *

class TrainInfo(object):
    """Name of the train along with his trainCode, Arrival Time Departure Time"""
    def __init__(self,trainCode,arrivalTime,departureTime,platformNo):
        self.trainCode = trainCode
        self.arrivalTime = arrivalTime
        self.departureTime = departureTime
        self.platformNo = platformNo

class TrainTableModel(QtCore.QAbstractTableModel):
    """Model class that drives the population of tabular display"""
    def __init__(self):
        super(TrainTableModel,self).__init__()
        self.headers = ['Code','Arrival','Departure','Pf']
        self.train  = []
 
    def rowCount(self,index=QtCore.QModelIndex()):
        return len(self.train)
 
    def addTrain(self,train):
        self.beginResetModel()
        self.train.append(train)
        self.endResetModel()
 
    def columnCount(self,index=QtCore.QModelIndex()):
        return len(self.headers)
 
    def data(self,index,role=Qt.DisplayRole):
        col = index.column()
        train = self.train[index.row()]
        if role == Qt.DisplayRole:
            if col == 0:
                return QVariant(train.trainCode)
            elif col == 1:
                return QVariant(train.arrivalTime)
            elif col == 2:
                return QVariant(train.departureTime)
            elif col == 3:
                return QVariant(train.platformNo)
            return QVariant()
 
    def headerData(self,section,orientation,role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
 
        if orientation == Qt.Horizontal:
            return QVariant(self.headers[section])
        return QVariant(int(section + 1))

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
        slider = QtGui.QSlider(1, self)
        slider.setRange(0, 2359)
        slider.setSingleStep(10)
        slider.resize(500, 20)
        slider.move(200, 57)

        # Start button
        sbtn = QtGui.QPushButton('Start Simulation', self)
        sbtn.setToolTip('Click to start simulation')
        sbtn.resize(sbtn.sizeHint())
        sbtn.move(50, 50)
        
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

        addTrainButton.move(screen.width()-350, screen.height()-250)
        deleteTrainButton.move(screen.width()-200, screen.height()-250)
        addPlatformButton.move(screen.width()-350, screen.height()-200)
        editPlatformButton.move(screen.width()-200, screen.height()-200)

        addTrainButton.clicked.connect(lambda: self.showAddTrainDialog())
        addPlatformButton.clicked.connect(lambda: self.showAddPlatformDialog())
        deleteTrainButton.clicked.connect(lambda: self.showDeleteTrainDialog())
        editPlatformButton.clicked.connect(lambda: self.showEditPlatformDialog())


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
            
        self.show()

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

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPlatforms(qp)
        self.drawOuterlines(qp)
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
            event.ignore()f

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



class AddTrainDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        super(AddTrainDialog,self).__init__(parent)

        self.layout = QtGui.QFormLayout(self)

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
        #Do something useful!
        QtGui.QDialog.accept(self)
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return

class DeleteTrainDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        super(DeleteTrainDialog,self).__init__(parent)

        layout = QtGui.QFormLayout(self)

        dropDownList = QtGui.QComboBox()
        trainList = ["12480","12481","12484"]
        dropDownList.addItems(trainList)

        buttonBox = QtGui.QDialogButtonBox()
        buttonOk = buttonBox.addButton("Delete Train",QtGui.QDialogButtonBox.AcceptRole)
        buttonCancel = buttonBox.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
        buttonOk.clicked.connect(lambda: self.buttonClickedOk())
        buttonCancel.clicked.connect(lambda: self.buttonClickedCancel())
        buttonBox.centerButtons

        layout.addRow(dropDownList)
        layout.addRow(buttonBox)

    def showDialog(parent = None):

        dialog = DeleteTrainDialog(parent)
        result = dialog.exec_()
        return

    def buttonClickedOk(self):
        #Do something useful!
        QtGui.QDialog.accept(self)
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return

class AddPlatformDialog(QtGui.QDialog):

    def __init__(self, parent=None):

        super(AddPlatformDialog,self).__init__(parent)

        layout = QtGui.QFormLayout(self)

        platformNumber = QtGui.QLineEdit()
        #trainName = QtGui.QLineEdit()

        buttonBox = QtGui.QDialogButtonBox()
        buttonOk = buttonBox.addButton("Add Platform",QtGui.QDialogButtonBox.AcceptRole)
        buttonCancel = buttonBox.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
        buttonOk.clicked.connect(lambda: self.buttonClickedOk())
        buttonCancel.clicked.connect(lambda: self.buttonClickedCancel())
        buttonBox.centerButtons()

        layout.addRow("Number of New Platforms",platformNumber)
        layout.addRow(buttonBox)

    def showDialog(parent = None):

        dialog = AddPlatformDialog(parent)
        result = dialog.exec_()
        return

    def buttonClickedOk(self):
        #Do something useful!
        QtGui.QDialog.accept(self)
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return

class EditPlatformDialog(QtGui.QDialog):

    def __init__(self,parent=None):
        super(EditPlatformDialog,self).__init__(parent)

        layout = QtGui.QFormLayout(self)

        platformList = []
        for i in range(1,17):
            platformList.append(QtGui.QCheckBox("Platform "+str(i)))
            layout.addRow(platformList[i-1])

        buttonBox = QtGui.QDialogButtonBox()
        buttonOk = buttonBox.addButton("Make Changes",QtGui.QDialogButtonBox.AcceptRole)
        buttonCancel = buttonBox.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
        buttonOk.clicked.connect(lambda: self.buttonClickedOk())
        buttonCancel.clicked.connect(lambda: self.buttonClickedCancel())
        buttonBox.centerButtons()

        layout.addRow(buttonBox)

    def showDialog(parent = None):

        dialog = EditPlatformDialog(parent)
        result = dialog.exec_()
        return

    def buttonClickedOk(self):
        #Do something useful!
        QtGui.QDialog.accept(self)
        return

    def buttonClickedCancel(self):
        #Do something useful!
        QtGui.QDialog.reject(self)
        return





def main():
    app = QtGui.QApplication(sys.argv)
    
    w = MainWin()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()