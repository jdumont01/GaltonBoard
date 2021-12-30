# importing libraries
# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QAction, QInputDialog

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIntValidator,QDoubleValidator

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QEvent

from math import *
import      random
import      matplotlib.pyplot as plt
import      plotly as pl
import      numpy as np
from        mpl_toolkits.mplot3d import axes3d, Axes3D
from        matplotlib.animation import FuncAnimation
import      matplotlib.animation as animation
from        matplotlib import cm
from        matplotlib.ticker import LinearLocator, FormatStrFormatter
import      matplotlib

_sysrand = random.SystemRandom()


__version__ = '0.1'
__author__ = 'Joe Dumont'

import random
import sys

# Use by the Board to determine how to process each ball event
class BallState():
    init = 'INIT'              # ball is ready 
    inProgress = 'INPROGRESS'  # ball is in play on board
    inProcess = 'INPROCESS'    # process of being counted
    complete = 'COMPLETE'      # ball has completed board
    lastBall = 'DONE'          # last ball to be processed
    
class BoardState():
    init = 'INIT'               # board is being initialized 
    inProgress = 'INPROGRESS'   # board is being drawn
    paused = 'PAUSED'           # board is paused    
    stopped = 'STOPPED'         # board activity has been stopped
    ready = 'READY'             # board is ready to be used
    
class statisticsView():

    def __init__(self, numEvents = 7, numSamples = 50):
        self._nEvents = numEvents
        self._nSamples = numSamples
        self._nTotalLeft = 0
        self._nTotalRight = 0
        self._sampleAry = np.empty((0, self._nEvents), np.int8)
        self._eventTotalAry = [0] * (self._nEvents + 1)
        self._nEventsLeft = 0
        self._nEventsRight = 0
        #print("Sample #", j)
        self._cntR = 0
        self._evtAry = ['-'] * (self._nEvents + 1)
        self._evtList = []

    def eventResult(self):
        """method can change the way the randmom number generator works."""
        return _sysrand.randint(0, 9)

    def updatePathList(self, result):
        """result will be """
        if result < 5:
            evtResult = "L"
            self._nEventsLeft += 1
            self._nTotalLeft += 1
        else:
            #print("Right")
            evtResult = "R"
            self._nEventsRight += 1
            self._nTotalRight += 1

        self._evtList.append(evtResult)
        #self._evtAry[i] = evtResult
        #print(evtAry)
        #print (evtList)

        return

    def resetEventList(self):
        self._nEventsLeft = 0
        self._nEventsRight = 0
        self._evtList = []
        
    def getBucketID(self):
        # Count the number of Right entries to determine which bucket receives the tally
        #print (self._cntR)
        self._cntR = self._evtList.count("R")
        
        return self._cntR 

    def clearBucketValues(self):
        self._eventTotalAry = [0] * (self._nEvents + 1)        
        
    def incrementBucketValue(self, bucket, n):
        self._eventTotalAry[bucket] = self._eventTotalAry[bucket] + 1
        
    def getBucketValue(self, bucket):
        return self._eventTotalAry[bucket]
        
    def returnPathList(self):        
        #print (self._evtList)
        return str(self._evtList)
                      
# creating game window
class GaltonBoardUi(QMainWindow):
    """Galton Board Main Window"""
    
    def __init__(self, board_depth = 7, eventTimer = 1, nBalls= 5, widthP = 800, heightP = 900):
        """View UI Initializer"""
        
        super(GaltonBoardUi, self).__init__()
        self._boardState = BoardState()
        self._currBoardState = self._boardState.init
        
        # Create the Menu
        self._createMenuActions()
        self._createMenuBar()
        self._connectMenuActions()
                
        self._boardDepth = board_depth
        self._boardWidthPx = widthP
        self._boardHeightPx = heightP
        self._pegCoords = []
        self.pegCoords = {}
        self._bucketCoords = []
        self._bucketContentCoords = []
        self._eventTimerInterval = eventTimer
        self.label = {}
        self.buckets = {}
        self._nBalls = nBalls  
        self._ballCtr = 0

        self._ballState = BallState()
        self._currBallState = self._ballState.init
        
        #ball coords
        self._boardHorBlocks = 0
        self._boardVertBlocks = 0
        self._blockHeightPx = 0 
        self._blockWidthPx = 0
        self._ballX = 0
        self._ballY = 0  #floor(self._boardHorBlocks/2)
        
        # Get a stats object
        self._stats = statisticsView(self._boardDepth, self._nBalls)
        
        # creating a board object
        # self.board = Board(self)

        # creating a timer
        self.timer = QBasicTimer()

        # creating a status bar to show result
        #self.statusbar = self.statusBar()
        
        # calling showMessage method when signal received by board
        #self.board.msg2statusbar[str].connect(self.statusbar.showMessage)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("border : 2px solid black;")
        self.statusBar.showMessage(f'Starting')
        
        # setting title to the window
        self.setWindowTitle('Galton Board')

        # setting geometry to the window
        #self.setGeometry(100, 100, 800, 800)
        self.setFixedSize(self._boardWidthPx, self._boardHeightPx)

        # adding board as a central widget
        #self._setCentralWidget(self.board)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        #self._createBoardHeader()
        #self._createUserMessageDisplay()
        #self._createPegBoard()
        #self._createResultsDisplay()
        self._initialize()

        # starting the board object
        #self.board.start()

        # showing the main window
        self.show()
        
    def _createMenuBar(self):
        """Create Menu Bar"""
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        # Creating menus using a title
        boardMenu = menuBar.addMenu("&Board")
        boardMenu.addAction(self.startAction)
        boardMenu.addAction(self.stopAction)
        boardMenu.addAction(self.resetAction)
        boardMenu.addSeparator()        
        boardMenu.addAction(self.pauseAction)
        boardMenu.addAction(self.resumeAction)
        boardMenu.addSeparator()
        boardMenu.addAction(self.exitAction)

        statisticsMenu = menuBar.addMenu("&Statistics")        

        helpMenu = menuBar.addMenu("&Help")        

    def _createMenuActions(self):
        """Create the Board Menu Options with keyboard shortcuts."""
        # Creating actions using the second constructor
        self.startAction = QAction("&Start", self)
        self.startAction.setShortcut("Ctrl+S")
        self.stopAction = QAction("S&top", self)
        self.stopAction.setShortcut("Ctrl+T")
        self.resetAction = QAction("&Reset", self)
        self.resetAction.setShortcut("Ctrl+R")
        self.pauseAction = QAction("&Pause", self)
        self.pauseAction.setShortcut("Ctrl+P")
        self.resumeAction = QAction("R&esume", self)
        self.resumeAction.setShortcut("Ctrl+E")
        self.exitAction = QAction("E&xit", self)
        self.exitAction.setShortcut("Ctrl+X")
        self.helpContentAction = QAction("&Help Content", self)
        self.helpContentAction.setShortcut("Ctrl+H")
        self.aboutAction = QAction("&About", self)
        self.aboutAction.setShortcut("Ctrl+A")
                
        return
        
    def _connectMenuActions(self):
        """Connect the menu options to the functions that contain the logic."""
        self.startAction.triggered.connect(self.startBoard)
        self.stopAction.triggered.connect(self.stopBoard)
        self.resetAction.triggered.connect(self.resetBoard)
        self.pauseAction.triggered.connect(self.pauseBoard)
        self.resumeAction.triggered.connect(self.resumeBoard)
        self.exitAction.triggered.connect(self.exitBoard)

    def startBoard(self):
        #print (f'In startBoard; board state = {self._currBoardState}')

        self._houseCleaning()
                
        # Board Depth
        num, ok = QInputDialog.getInt(self, "Board Depth Dialog", "Enter the Board Depth")

        if ok:
            self._setBoardDepth(num)
            #self._inputBoardDepthBox.setText(f'Depth = {self._getBoardDepth()}')
        else:
            self.statusBar.showMessage(f'Invalid Board Depth Input')

        # Number of Balls
        num, ok = QInputDialog.getInt(self, "Number of Tests Dialog", "Enter the Number of Balls")

        if ok:
            self._setNumBalls(num)
            #self._inputNumBallsBox.se.reatText(f'Depth = {self._getNumBalls()}')
        else:
            self.statusBar.showMessage(f'Invalid Ball Number Input')
        
        #print(f'Current Board state is {self._currBoardState}')
        
        if (self._currBoardState == self._boardState.stopped or
            self._currBoardState == self._boardState.paused or 
            self._currBoardState == self._boardState.ready):
            self._currBoardState = self._boardState.stopped
        else:
            self._currBoardState = self._boardState.init
        
        self._start()
        
    def _houseCleaning(self):
        # Housecleaning
        if (self._currBoardState == self._boardState.inProgress or
            self._currBoardState == self._boardState.stopped or
            self._currBoardState == self._boardState.ready):
            #Clear widgets from each layouts
            self._clearResultsDisplay()
            self._clearPegBoard()
            self._clearLayout(self.generalLayout)
            del self._stats 
        else:
            print(f'Do nothing for now')
            
        return
   
    def stopBoard(self):
        print (f'In stopBoard')
        self._messageBox.setText(f'Stopping.....Will implement saving results later.')
        self._currBoardState = self._boardState.stopped
        self.timer.stop()
        
    def resetBoard(self):
        #print (f'In resetBoard; board state = {self._currBoardState}')
        if (self._currBoardState == self._boardState.stopped or
            self._currBoardState == self._boardState.ready):
            self._messageBox.setText(f'Resetting Board Statistics.')
            self.timer.stop()
            self._houseCleaning()
            self._start()
        
    def pauseBoard(self):
        print (f'In pauseBoard')
        self._currBoardState = self._boardState.paused
        self.timer.stop()

    def resumeBoard(self):
        print (f'In pauseBoard')
        if (self._currBoardState == self._boardState.stopped or 
            self._currBoardState == self._boardState.paused):
            self.timer.start(self._eventTimerInterval, self)

    def exitBoard(self):
        print (f'In exitBoard')
        self.close()
        
    def helpContent(self):
        print (f'In helpContent')
        
    def aboutContent(self):
        print (f'In aboutAction')
    
    def _initialize(self):
        self.statusBar.showMessage(f'Select Board --> Start to start the Galton Board.')
        self._ballCtr = 0
        self._currBallState = self._ballState.init
        
        #ball coords
        self._ballX = 0
        self._ballY = floor(self._boardHorBlocks/2)

    def _restart(self):
        print (f'board state = {self._currBoardState}')
        
        if self._currBoardState == self._boardState.ready:
            #Clear widgets from each layouts
            self._houseCleaning()
            self._createBoardHeader()        
            self._createPegBoard()
            self._createResultsDisplay()
            self._stats = statisticsView(self._boardDepth, self._nBalls)

        return
        
    def _start(self):
        """Start the board events."""        
        print (f'In _start; board state = {self._currBoardState}')
        self._boardHorBlocks, self._boardVertBlocks = self._calculateBoardGridSize()
        self._blockHeightPx, self._blockWidthPx = self._calculateBlockSize()

        if self._currBoardState == self._boardState.init:
            self._stats = statisticsView(self._boardDepth, self._nBalls)
            self._createBoardHeader()        
            self._createPegBoard()
            self._createResultsDisplay()
        elif (self._currBoardState == self._boardState.inProgress or
            self._currBoardState == self._boardState.stopped or
            self._currBoardState == self._boardState.ready):
            #Clear widgets from each layouts
            #self._clearPegBoard()
            #self._clearLayout(self.generalLayout)
            self._stats = statisticsView(self._boardDepth, self._nBalls)
            self._createBoardHeader()        
            self._createPegBoard()
            self._createResultsDisplay()
        else:
            print(f'Do nothing for now')

        # Initialize the bucket values
        self._initBucketValues()
        self._initialize()

        self._currBoardState = self._boardState.ready
        self.timer.start(self._eventTimerInterval, self)
        
        return

    # time event method
    def timerEvent(self, event):
  
        # checking timer id
        if event.timerId() == self.timer.timerId():
            self.statusBar.showMessage(f'Timer Event {event} | Current State of Ball {self._currBallState}')
            #print (self._getBallState())
            #print (self._stats.returnPathList())
            #self.timer.stop()                    

            # Ball state types from BallState class
            # INIT
            if self._getBallState() == self._ballState.init:
                self._setCurrentBallCount(self._ballCtr + 1)
                self.statusBar.showMessage(f'Timer Event | Current State of Ball is Ready')                
                self.label[self._createKeyFromCoords(self._ballX, self._ballY)].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  
                self._stats.resetEventList()
                self._setBallState(self._ballState.inProgress)
                # starting timer
                self.timer.start(self._eventTimerInterval, self)
            # INPROGRESS
            elif self._getBallState() == self._ballState.inProgress:
                #Check on position
                #print(f'check: {self._ballX} {self._boardVertBlocks - 1}')
                # if the ball is done, reset and start next ball
                if self._ballX == self._boardVertBlocks - 1:
                    self.label[self._createKeyFromCoords(self._ballX, self._ballY)].clear()
                    self._setBallState(self._ballState.inProcess)   
                elif self._getBallCoords() in self._pegCoords:
                    self.statusBar.showMessage(f'Timer Event | Current State of Ball Coords: {self._getBallCoords()}')
                    # move to next coord
                    rndN = self._stats.eventResult()
                    #print (rndN)
                    if rndN < 5:
                        #print("Left")
                        self._stats.updatePathList(rndN)
                        self._setBallCoords((self._ballX - 1), (self._ballY - 1))
                    else:
                        #print("Right")
                        self._stats.updatePathList(rndN)
                        self._setBallCoords((self._ballX - 1), (self._ballY + 1))
                    self.label[self._createKeyFromCoords(self._ballX, self._ballY)].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  
                    self.statusBar.showMessage(f'Timer Event | Current Stats:  ')                
                else:
                    self.statusBar.showMessage(f'Timer Event | Current State of Ball Coords: {self._ballX}, {self._ballY}')
                    self.label[self._createKeyFromCoords(self._ballX, self._ballY)].clear()
                    self._setBallCoords(self._ballX + 1, self._ballY)
                    self.label[self._createKeyFromCoords(self._ballX, self._ballY)].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  

                self._messageBox.setText(f'Ball # {self._getCurrentBallCount()} updated path {self._stats.returnPathList()}')
                self.timer.start(self._eventTimerInterval, self)                    

            # INPROCESS
            # process the stats for the ball that just finished
            elif self._getBallState() == self._ballState.inProcess:
                self.statusBar.showMessage(f'Timer Event | Current State of Ball : {self._currBallState}')
                self._messageBox.setText(f'Ball # {self._getCurrentBallCount()} out of {self._nBalls}')
                # finish if the last ball has been processed
                if self._getCurrentBallCount() != self._nBalls:
                    self._setBallState(self._ballState.init)   
                    self._resetBallPosition()
                else:
                    self._setBallState(self._ballState.lastBall)
                
                # Determine which bucket is being updated
                self._stats.incrementBucketValue(self._stats.getBucketID(), 1)
                self.buckets[self._stats.getBucketID()].setText(f'{self._stats.getBucketValue(self._stats.getBucketID())}')
                
                self.timer.start(self._eventTimerInterval, self)

            # LASTBALL
            elif self._getBallState() == self._ballState.lastBall:
                self.statusBar.showMessage(f'Timer Event | Current State of Ball : {self._currBallState}')
                self._messageBox.setText(f'Last Ball.....Done')
                self._currBoardState == self._boardState.stopped
                self.timer.stop()
            else:
                self.statusBar.showMessage(f'Timer Event | Current State {self._currBallState} does not exist.')
            # update the window
            self.update()

    def _clearLayout(self, layout):
        """Remove widgets from layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    layout.removeWidget(widget)
                    #widget.setParent(None)
                else:
                    self._clearLayout(item.layout())        

    def _clearWidgetsFromLayout(self, layout):
    
        for j in reversed(range(layout.count())): 
            #print (f'{j}')
            widgetToRemove = layout_item.itemAt(j).widget()
            
            if widgetToRemove is not None:
                # remove it from the layout list
                layout_item.removeWidget(widgetToRemove)
                # remove it from the gui
                widgetToRemove.setParent(None)
                    
        return
        
    def _setCurrentBallCount(self, n):
        self._ballCtr = n
        
    def _getCurrentBallCount(self):
        return self._ballCtr
        
    def _setBoardDepth(self, n):
        self._boardDepth = n

    def _getBoardDepth(self):
        return self._boardDepth
        
    def _setNumBalls(self, n):
        self._nBalls = n 
    
    def _getNumBalls(self):
        return self._nBalls

    def _resetBallPosition(self):
        self._ballX = 0
        self._ballY = floor(self._boardHorBlocks/2)

    def _setBallState(self, state):
        self._currBallState = state
        
    def _getBallState(self):
        return self._currBallState
        
    def _setBallCoords(self, x, y):
        self._ballX = x
        self._ballY = y
        
        return
    
    def _getBallCoords(self):
        #print (f'{self._ballX}, {self._ballY}')
        return self._ballX, self._ballY
               
    def _calculateBoardGridSize(self):
        """Determine how many grid elements are needed based on
        Board depth."""
        nHorizontalBlocks = 2 * self._boardDepth + 1
        nVerticalBlocks = 2 * self._boardDepth + 2
        
        return nHorizontalBlocks, nVerticalBlocks
        
    def _calculateBlockSize(self):
        """Size the Galton Board widgets based on depth"""
        # assume square for now
        blockWidth = blockHeight = floor(sqrt((self._boardHeightPx * self._boardWidthPx)/(self._boardHorBlocks * self._boardVertBlocks)))
        
        return blockWidth, blockHeight
        
    def _createUserMessageDisplay(self):
        """This display updates the user with the current status of the events."""
        self._messageBox = QLineEdit()
            
        # Basic layout params
        self._messageBox.setFixedHeight(25)
        self._messageBox.setAlignment(Qt.AlignLeft)
        self._messageBox.setReadOnly(True)
        self._messageBox.setFont(QFont("Arial",15))

        # Add to the general layout
        #self.generalLayout.addWidget(self._messageBox)
        self._boardHeaderLayout.addWidget(self._messageBox, 0, 0)

        return

    def _createBoardHeader(self):
        self._boardHeaderLayout = QGridLayout()
        self._boardHeaderCoords = {}
        #self._boardHeaderLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # Create Output Message box for the user
        self._messageBox = QLineEdit()
            
        # Basic layout params
        self._messageBox.setFixedHeight(25)
        self._messageBox.setAlignment(Qt.AlignLeft)
        self._messageBox.setFixedWidth(self._boardWidthPx)
        self._messageBox.setReadOnly(True)
        self._messageBox.setFont(QFont("Arial",15))

        # Add to the general layout
        self._boardHeaderLayout.addWidget(self._messageBox, 0, 0)

        # Create Input box to enter board depth
        self._inputBoardDepthBox = QLineEdit()
            
        # Basic layout params
        self._inputBoardDepthBox.setFixedHeight(25)
        self._inputBoardDepthBox.setValidator(QIntValidator())
        self._inputBoardDepthBox.setAlignment(Qt.AlignHCenter)
        self._inputBoardDepthBox.setFixedWidth((floor(self._boardHorBlocks/2) - 1) * self._blockWidthPx)
        self._inputBoardDepthBox.setFont(QFont("Arial",15))
        self._inputBoardDepthBox.setText(f'Depth = {self._boardDepth}')
        # Add to the general layout
        self._boardHeaderLayout.addWidget(self._inputBoardDepthBox, 1, 0)
        
        # Create Input box to enter the number of balls
        self._inputNumBallsBox = QLineEdit()
            
        # Basic layout params
        self._inputNumBallsBox.setFixedHeight(25)
        self._inputNumBallsBox.setValidator(QIntValidator())
        self._inputNumBallsBox.setAlignment(Qt.AlignHCenter)
        self._inputNumBallsBox.setFixedWidth((floor(self._boardHorBlocks/2) - 1) * self._blockWidthPx)
        self._inputNumBallsBox.setReadOnly(False)
        self._inputNumBallsBox.setFont(QFont("Arial",15))
        self._inputNumBallsBox.setText(f'Number of Balls = {self._nBalls}')
        # Add to the general layout
        self._boardHeaderLayout.addWidget(self._inputNumBallsBox, 1, 1)

        self.generalLayout.addLayout(self._boardHeaderLayout)
                
    def _clearPegBoard(self):
        print(f'In _clearPegBoard')
        if self._pegLayout is not None:
            for key, _ in self.pegCoords.items():   
                #print (f'key = {key}')
                self.label[key].clear()
                if self.label[key] is not None:
                    #print (f'Removing {self.label[key]}')
                    self._pegLayout.removeWidget(self.label[key]) 

        self._clearPegCoords()
        self.generalLayout.removeItem(self._pegLayout)
        
        return
    
    def _createPegBoard(self):
        """Creates the Galton Board"""
        self._pegLayout = QGridLayout()
        self.pegCoords = {}
        
        boardContentCoords = [(x,y) for x in range (self._boardVertBlocks) for y in range(self._boardHorBlocks)]
        for x, y in boardContentCoords:
            self.pegCoords[self._createKeyFromCoords(x,y)] = (x,y)
            
        #print (self.pegCoords)
            
        self._setPegCoords()
        #print (self._pegCoords)
                
        # Create first and list rows' figures
        for key, coords in self.pegCoords.items():
            #print (coords)
            self.label[key] = QLabel(self)
            if coords[0] == 0:
                if coords[1] != floor(self._boardHorBlocks/2):
                    self.label[key].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\horizontal-line.png"))
                    self.label[key].setAlignment(Qt.AlignLeft)
            elif coords[0] == self._boardVertBlocks - 1:
                if coords[1] % 2 == 1:
                    self.label[key].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\vertical_line.png"))
                    self.label[key].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            else:
                if coords in self._pegCoords:
                    #print (f'[{x}, {y}]')
                    self.label[key].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))
                    self.label[key].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    
            self.label[key].setFixedSize(self._blockWidthPx, self._blockHeightPx)
            self.label[key].setScaledContents(True)
            #label.setSpacing(0)
            self.label[key].setContentsMargins(0, 0, 0, 0)
            self._pegLayout.addWidget(self.label[key], coords[0], coords[1])
                                
        # Add to general layout
        self.generalLayout.addLayout(self._pegLayout)
        
        return
        
    def _createKeyFromCoords(self, x, y):
        """Create the key value based on the provided coordinates."""     
        return f'x{x}y{y}'
        
    def _setPegCoords(self):
        """ Calcualtes the coordinates for each peg."""
        for i in range(self._boardVertBlocks):
            if i%2 == 0:
                for j in range(0, (floor(i/2))):
                    p = self._boardDepth - (floor(i/2)) + 1 + (2 * j)
                    self._pegCoords.append((i, p))
                        
        return
        
    def _clearPegCoords(self):
        self._pegCoords = []
        
        return
        
    def _clearResultsData(self):
        if self._bucketLayout is not None:
            for key, _ in self._bucketCoords.items():
                #print (f'key = {key}')
                self.buckets[key].setText(f'0')
    
        return
        
    def _clearResultsDisplay(self):
        print(f'In _clearResultsDisplay')
        if self._bucketLayout is not None:
            for key, _ in self._bucketCoords.items():
                #print (f'key = {key}')
                self.buckets[key].clear()
                if self.buckets[key] is not None:
                    #print (f'Removing {self.buckets[key]}')
                    self._bucketLayout.removeWidget(self.buckets[key])    
                    
            self._stats.clearBucketValues()
                    
            self._clearBucketCoords()
            self.generalLayout.removeItem(self._bucketLayout)
        
        return
        
    def _clearBucketCoords(self):
        self._bucketCoords = {}
        self._bucketContentCoords = []
        
    def _createResultsDisplay(self):
        """This display updates the user with the current status of the events."""
        self._bucketLayout = QGridLayout()
        self._bucketCoords = {}
        
        self._bucketLayout.setSpacing(self._blockWidthPx)
        
        self._bucketContentCoords = [ (self._boardHorBlocks, y) for y in range(self._boardHorBlocks)]
        for x,y in self._bucketContentCoords:
            # calculate and the bucket id as the key - 0, 1, 2 etc
            # to align with the logic for counting R's
            if y%2 == 0:
                self._bucketCoords[floor(y/2)] = (x,y)
          
        # Need to display blank blocks along side the Edit boxes
        for key, coords in self._bucketCoords.items():
            #print (f'key = {key}')
            self.buckets[key] = QLineEdit(self)            
            # Basic layout params   
            self.buckets[key].setFixedHeight(50)
            self.buckets[key].setFixedWidth(self._blockWidthPx)
            self.buckets[key].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.buckets[key].setReadOnly(True)
            self.buckets[key].setFont(QFont("Arial",15))
            self.buckets[key].setContentsMargins(0, 0, 0, 0)
            #self.buckets[key].setToolTip(f'Value = {self.buckets[key].text()}')
            #self.buckets[key].installEventFilter(self)

            self._bucketLayout.addWidget(self.buckets[key], coords[0], coords[1])

        # Add to the general layout
        self.generalLayout.addLayout(self._bucketLayout)

        return
        
    def _initBucketValues(self):
        """This function initializes the values of each bucket."""
        for key, _ in self._bucketCoords.items():
            #print (f'{key}')
            self.buckets[key].setText(f"0")
            
            
    # *****************    
    # Public Interfaces
    # *****************        
    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText('')    



class Board(QFrame):
    # creating signal object
    msg2statusbar = pyqtSignal(str)

    # speed of the snake
    # timer countdown time
    SPEED = 1000

    # constructor
    def __init__(self, parent):
        super(Board, self).__init__(parent)

        # creating a timer
        self.timer = QBasicTimer()

        # Prepare peg tree; dict index = peg numb, value = row, col coords
        self.snake = []

        # setting focus
        self.setFocusPolicy(Qt.StrongFocus)

    def initializeBoard(self):
        """
        Setup the Galton board.
        """
        
        # setup tree
        # Each peg will be surrounded by 1 square so that the ball can recoil and move 
        # either to the left or the right
        
    
    # start method
    def start(self):
        # msg for status bar
        # score = current len - 2
        # self.msg2statusbar.emit(str(len(self.snake) - 2))
        self.msg2statusbar.emit(str("Starting"))

        # starting timer
        self.timer.start(Board.SPEED, self)

    # time event method
    def timerEvent(self, event):

        # checking timer id
        if event.timerId() == self.timer.timerId():
            self.msg2statusbar.emit(str("Timer Event"))

            # update the window
            self.update()

# Client side code
def main():
    app = QApplication(sys.argv)
    view = GaltonBoardUi(board_depth=3, nBalls = 30)
    view.show()
    sys.exit(app.exec_())


# main method
if __name__ == '__main__':
    main()