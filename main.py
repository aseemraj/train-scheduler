import sys, random
from PyQt4 import QtCore, QtGui

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
        qbtn.move(screen.width()-200, screen.height()-120)

        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPlatforms(qp)
        self.drawOuterlines(qp)
        qp.end()
        
    def drawPlatforms(self, qp):
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)

        for i in range(8):
            qp.setBrush(QtGui.QColor(50, 50, 50))
            qp.drawRect(100, 230+i*60, 600, 15)
            qp.setBrush(QtGui.QColor(20, 20, 20))
            qp.drawRect(100, 230+i*60+15, 600, 15)
    
    def drawOuterlines(self, qp):
        color = QtGui.QColor(0, 100, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)

        for i in range(5):
            qp.setBrush(QtGui.QColor(50, 100, 50))
            qp.drawRect(50, 130+i*10, 200, 5)
        for i in range(5):
            qp.setBrush(QtGui.QColor(50, 100, 50))
            qp.drawRect(550, 130+i*10, 200, 5)
            # qp.setBrush(QtGui.QColor(20, 20, 20))
            # qp.drawRect(100, 130+i*10+5, 600, 5)
        
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