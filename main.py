import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
        self.headers = ['Train Code','Arrival Time','Departure Time','PlatForm No']
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
        qbtn.resize(sbtn.sizeHint())
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.move(screen.width()-170, screen.height()-120)

        #Adding Train To Table
        view = QTableView(self)
        tableData = TrainTableModel()
        view.setModel(tableData)
        view.setGeometry(screen.width()-460,0,400,600)
 
        tableData.addTrain(TrainInfo('12480', '11:00 AM', '11:10 AM','4'))
        tableData.addTrain(TrainInfo('12480', '11:00 AM', '11:10 AM','4'))
        tableData.addTrain(TrainInfo('12480', '11:00 AM', '11:10 AM','4'))

        self.show()
        
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

def main():
    app = QtGui.QApplication(sys.argv)
    
    w = MainWin()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()