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
from PyQt5.QtWidgets import QMessageBox

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIntValidator,QDoubleValidator

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QBasicTimer, QTimer
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
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import pandas
from collections import Counter

import      sys

_sysrand = random.SystemRandom()


__version__ = '0.9'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

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

class MplCanvas(FigureCanvasQTAgg):
    """General use class to display matplotlib objects"""
    """Ref https://www.pythonguis.com/tutorials/plotting-matplotlib/ """
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class statisticsView(QMainWindow):
    """Display all stats."""
    def __init__(self, parent=None, refreshPeriod = 100):
        super(statisticsView, self).__init__(parent)
        
        self._refreshPeriod = refreshPeriod
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("border : 2px solid black;")
        self.statusBar.showMessage(f'Starting')
        
        # setting title to the window
        self.setWindowTitle('Galton Board Results')

        # setting geometry to the window
        self.setGeometry(100, 100, 800, 800)
        #self.setFixedSize(self._boardWidthPx, self._boardHeightPx)
        
        # This class can display the results array and the expected results
        # in a histogram from numpy
               
        # creating a timer
        #self.refreshTimer = QTimer()
        #self.refreshTimer.timeout.connect(self.update)        
        
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self._sc = MplCanvas(self, width=5, height=4, dpi=100)
        self._sc.mpl_connect("motion_notify_event", self._hover)
        
        # default - will be configured later
        self.annot = self._sc.axes.annotate("", xy=(0,0),textcoords="offset points",
                bbox=dict(boxstyle="round", fc="black", ec="b", lw=2),
                arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        
        # toolbar for the graph UI
        self._toolbar = NavigationToolbar(self._sc, self)
        
        # Create layout
        self._graphLayout = QVBoxLayout()
        self._graphLayout.addWidget(self._toolbar)
        self._graphLayout.addWidget(self._sc)
        
        # hold toolbar
        self._graphWidget = QWidget()
        self._graphWidget.setLayout(self._graphLayout)
        self.setCentralWidget(self._graphWidget)
        
        self._initialize()
        
        return
        
    def __del__(self):
        #del self._sc  
        
        return
    
    def _hover(self, event):
        """Return the value that the mouse is hovering over."""
        # event has motion_notify_event:  xy, xydata, button, dblclick, inaxes
        #vis = self.annot.get_visible()
        print (f'_hover event = {event}')

        if event.inaxes == self._sc.axes:
            print(f'event triggered')
            print(f'{event.xdata}, {event.xdata}, {self._sc.axes}, {self._plot}')
            #if event in self._plot:
            print(f'in update')
            #cont, ind = self._plot.contains(event)
            #if cont:
            self._update_annot(event)
            self.annot.set_visible(True)
            self._sc.draw_idle()
        else:
            self.annot.set_visible(False)                
            
        #if vis:
        #    self.annot.set_visible(False)
        #    self._sc.draw_idle()        
        
        return

    def _update_annot(self, event):
        """Print the annotated data."""
        print(f'in _update_annot')
        x = event.xdata
        y = event.ydata
        self.annot.xy = (x,y)
        text = "({:d},{:d})".format(int(x),int(y))
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

        return
        
    def _initialize(self):
        #self.refreshTimer.start(self._refreshPeriod)               
        
        return

    def update(self):
        self.refreshTimer.stop()
        self.refreshResultsHistogram()
        
        return
        
    # time event method
    def timerEvent(self, event):
        # checking timer id
        if event.timerId() == self.refreshTimer.timerId():
            print (f'Refresh Timer triggered')
            self.statusBar.showMessage(f'Timer Event {event} ')
        
        return
        
    def _getPlotText(self):
        self._sc.axes.set_title('Results from Galton Board')
        self._sc.axes.set_xlabel('Bucket Number')
        self._sc.axes.set_ylabel('Frequency')

        return
        
    def refreshResultsHistogram(self, data):
        #print (f'refreshResultsHistogram {data}')
        bins = []
        hist = []
        binsOut = []
        
        #self._sc.axes.clear()
        #self._sc.axes.set_frame_on(True)
        #self._sc.axes.set_axis_on()
        #self._sc.axes.grid(True)
        self._sc.axes.cla()
        self._getPlotText()
        
        for i in range(len(data)):
            bins.append(i)
            
        hist, binsOut = np.histogram(data, bins=bins)
        #print (f'data = {data}')
        #print (f'hist = {hist}')
        #print (f'bins = {binsOut}')
        
        self._plot = self._sc.axes.plot(bins, data, '-', color='blue')
        #self.setCentralWidget(self._sc)        
        self.annot = self._sc.axes.annotate("", xy=(0,0),textcoords="offset points",
                xytext=(50, 50), bbox=dict(boxstyle="round", fc="black", ec="b", lw=2),
                arrowprops=dict(arrowstyle="->"))

        self._sc.draw()
    
        return
        
    def displayResultsHistogram(self, data):
        """displayResultsHistogram"""
        bins = []

        self._getPlotText()
        
        for i in range(len(data)):
            bins.append(i)
            
        hist, binsOut = np.histogram(data, bins=bins)
        #print (f'data = {data}')
        #print (f'hist = {hist}')
        #print (f'bins = {binsOut}')
        
        self._plot = self._sc.axes.plot(bins, data, '-', color='blue')
        
        #self.setCentralWidget(self._sc)
        
        self._sc.show()
   
class GaltonBoardResultTracking():
    """Calculate and display all stats."""
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
    
    def getResultsArray(self):
        print (f'In getResultsArray: {self._eventTotalAry}')
        return self._eventTotalAry
        
    def getResultsInLists(self):
        
        #for key in range(self._eventTotalAry):
        #print (f'{key}, {self._eventTotalAry[key]}')
        print (f'{self._eventTotalAry}')
        return
        
class GaltonBoardBall():
    """Ball class when the Galton Board supports multiple in-play balls."""
    def __init__(self, xValue = 0, yValue = 0):
        self._ballState = BallState()
        self._currState = self._ballState.init
        self._currXValue = xValue
        self._currYValule = yValue
        
    def setBallState(self, state):
        if state in [self._ballState.init, self._ballState.inProgress, self._ballState.inProcess, self._ballState.complete, self._ballState.lastBall]:
            self._currBallState = state
        else:
            print(f'Ball state {state} is invalid.')
            
        return
        
    def getBallState(self):
        return self._currBallState
        
    def setBallCoords(self, x, y):
        if x >= 0:
            self._ballX = x
        else:
            print(f'x coordinate must be >= 0')
            
        if y>= 0:
            self._ballY = y        
        else:
            print(f'y coordinate must be >= 0')
        
        return
    
    def getBallCoords(self):
        #print (f'{self._ballX}, {self._ballY}')
        return self._ballX, self._ballY

    def getBallXCoord(self):
        #print (f'In getBallXCoord: {self._ballX}')
        return self._ballX

    def getBallYCoord(self):
        #print (f'In getBallYCoord: {self._ballY}')
        return self._ballY
               
# creating game window
class GaltonBoardUi(QMainWindow):
    """Galton Board Main Window"""
    
    def __init__(self, board_depth = 7, parent=None, eventTimer = 1, nBalls= 5, widthP = 800, heightP = 900, bDebug = True):
        """View UI Initializer"""
        
        super(GaltonBoardUi, self).__init__(parent)
        self._boardState = BoardState()
        self._currBoardState = self._boardState.init
        
        # set consts
        self.DEFAULT_BOARD_DEPTH = 7
        self.DEFAULT_EVENT_TIMER = 100
        self.DEFAULT_NUMBER_OF_BALLS = 100
        
        # Create the Menu
        self._createMenuActions()
        self._createMenuBar()
        self._connectMenuActions()
                
        self._boardDepth = board_depth
        self._boardWidthPx = widthP
        self._boardHeightPx = heightP
        self._globalDebug = bDebug
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
        self._ball = GaltonBoardBall(xValue = 0, yValue = 0)
        self._ball.setBallState(self._ballState.init)
        
        #ball coords
        self._boardHorBlocks = 0
        self._boardVertBlocks = 0
        self._blockHeightPx = 0 
        self._blockWidthPx = 0
        #self._ballX = 0
        #self._ballY = 0  #floor(self._boardHorBlocks/2)
        
        # Get a stats object
        self._stats = GaltonBoardResultTracking(self._boardDepth, self._nBalls)
        
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

        # track all stats UIs
        self.statUiList = list()
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

        # creating a timer to refresh stats
        self.resultsDisplay = statisticsView(self)
        self.refreshTimer = QTimer()
        self.refreshTimer.timeout.connect(self._refreshStatsView)  
        self._refreshStatsPeriod = 5000

        self._initialize()

        # starting the board object
        #self.board.start()

        # showing the main window
        self.show()
        
        return

    def __del__(self):
        """Galton Board Destructor"""
        self._currBoardState = self._boardState.stopped
        self.timer.stop()
        self.refreshTimer.stop()
        
        for item in self.statUiList:
            self.statUiList.remove(item)
                  
        #self._houseCleaning()
        
        return

    def _refreshStatsView(self):
        """Call the Views verson of refreshing the stats UI"""
        self.refreshTimer.stop()
        self.resultsDisplay.refreshResultsHistogram(self._stats.getResultsArray())
        self.resultsDisplay.show()
        self.refreshTimer.start(self._refreshStatsPeriod)       

        return
        
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
        statisticsMenu.addAction(self.showStatisticsViewAction)

        helpMenu = menuBar.addMenu("&Help")        
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addSeparator()
        helpMenu.addAction(self.startAboutContent)
        
        gettingStartMenu = menuBar.addMenu("&Getting Started")

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
        
        self.showStatisticsViewAction = QAction("Res&ults", self)
        self.showStatisticsViewAction.setShortcut("Ctrl+U")

        self.helpContentAction = QAction("&Help Content", self)
        self.helpContentAction.setShortcut("Ctrl+H")
        self.startAboutContent = QAction("&About", self)
        self.startAboutContent.setShortcut("Ctrl+A")

        self.gettingStartedAction = QAction("&Getting Started", self)
        self.gettingStartedAction.setShortcut("Ctrl+G")
                
        return
           
    def _connectMenuActions(self):
        """Connect the menu options to the functions that contain the logic."""
        # Board Menu Options
        self.startAction.triggered.connect(self.startBoard)
        self.stopAction.triggered.connect(self.stopBoard)
        self.resetAction.triggered.connect(self.resetBoard)
        self.pauseAction.triggered.connect(self.pauseBoard)
        self.resumeAction.triggered.connect(self.resumeBoard)
        self.exitAction.triggered.connect(self.exitBoard)
        
        # Statistics Menu Options
        self.showStatisticsViewAction.triggered.connect(self.createResultsView)
        
        # Help Menu Options
        self.startAboutContent.triggered.connect(self.startAbout)
  
    def createResultsView(self):
        """Show results"""
        self.statUiList.append(self.resultsDisplay)
        self.resultsDisplay.displayResultsHistogram(self._stats.getResultsArray())
        self.resultsDisplay.show()
        
        return       

    def startAbout(self):
        """ """
        s = f'Galton Board Version:  {__version__}\nAuthor:  {__author__}\nReleased:  {__releaseDate__}\nPython Version:  {sys.version}\nVersion Info:  {sys.version_info}'
        QMessageBox.about(self, "About Galton Board", s) 
        #msg.setIcon(QMessageBox.Information)
        #msg.setStandardButtons(QMessageBox.Ok)
        
        return

    def startBoard(self):
        print (f'In startBoard; board state = {self._currBoardState}')

        # Board Depth
        num, ok = QInputDialog.getInt(self, "Board Depth Dialog", "Enter the Board Depth", self.DEFAULT_BOARD_DEPTH)

        if ok:
            self._setBoardDepth(num)
            #self._inputBoardDepthBox.setText(f'Depth = {self._getBoardDepth()}')
        else:
            self.statusBar.showMessage(f'Invalid Board Depth Input')

        # Number of Balls
        num, ok = QInputDialog.getInt(self, "Number of Tests Dialog", "Enter the Number of Balls", self.DEFAULT_NUMBER_OF_BALLS)

        if ok:
            self._setNumBalls(num)
            #self._inputNumBallsBox.se.reatText(f'Depth = {self._getNumBalls()}')
        else:
            self.statusBar.showMessage(f'Invalid Ball Number Input')       

        # Event timer
        num, ok = QInputDialog.getInt(self, "Set Event Timer", "Set Event Timer (ms)", self.DEFAULT_EVENT_TIMER)

        if ok:
            self._setEventTimerInterval(num)
            #self._inputNumBallsBox.se.reatText(f'Depth = {self._getNumBalls()}')
        else:
            self.statusBar.showMessage(f'Invalid Time Input')
        
        #print(f'Current Board state is {self._eventTimerInterval}')
        
        # reset board state
        if (self._currBoardState in [self._boardState.stopped, self._boardState.paused, self._boardState.ready]):
            self._currBoardState = self._boardState.stopped
        else:
            self._currBoardState = self._boardState.init
        
        self._start()
        
    def _houseCleaning(self):
        # Housecleaning
        if (self._currBoardState in [self._boardState.stopped, self._boardState.inProgress, self._boardState.ready]):
            #Clear widgets from each layouts
            self._clearResultsDisplay()
            self._clearPegBoard()
            self._clearLayout(self.generalLayout)
            del self._stats 
        else:
            print(f'Do nothing for now for Board State {self._currBoardState}')
            
        return
   
    def stopBoard(self):
        print (f'In stopBoard')
        self._messageBox.setText(f'Stopping.....Will implement saving results later.')
        self._currBoardState = self._boardState.stopped
        #self._houseCleaning()
        self.timer.stop()
        
    def resetBoard(self):
        #print (f'In resetBoard; board state = {self._currBoardState}')
        if (self._currBoardState in [self._boardState.stopped, self._boardState.ready]):
            self._messageBox.setText(f'Resetting Board Statistics.')
            self.timer.stop()
            self._houseCleaning()
            self._start()
        
    def pauseBoard(self):
        print (f'In pauseBoard')
        self._currBoardState = self._boardState.paused
        self.timer.stop()

    def resumeBoard(self):
        print (f'In resumeBoard')
        if (self._currBoardState in [self._boardState.stopped, self._boardState.paused]):
            self._currBoardState = self._boardState.ready
            self.timer.start(self._eventTimerInterval, self)

    def exitBoard(self):
        print (f'In exitBoard')
        self._currBoardState = self._boardState.stopped
        self.timer.stop()
        self.close()
        
    def helpContent(self):
        print (f'In helpContent')
        
    def _initialize(self):
        self.statusBar.showMessage(f'Select Board --> Start to start the Galton Board.')
        self._ballCtr = 0
        #self._currBallState = self._ballState.init
        self._ball.setBallState(self._ballState.init)

        #ball coords
        self._ball.setBallCoords(0, floor(self._boardHorBlocks/2))

        #self._ballX = 0
        #self._ballY = floor(self._boardHorBlocks/2)
                
        self.refreshTimer.start(self._refreshStatsPeriod)       

        return  

    def _restart(self):
        print (f'board state = {self._currBoardState}')
        
        if self._currBoardState == self._boardState.ready:
            #Clear widgets from each layouts
            self._houseCleaning()
            self._createBoardHeader()        
            self._createPegBoard()
            self._createResultsDisplay()
            self._stats = GaltonBoardResultTracking(self._boardDepth, self._nBalls)

        return
        
    def _start(self):
        """Start the board events."""        
        print (f'In _start; board state = {self._currBoardState}')
        self._boardHorBlocks, self._boardVertBlocks = self._calculateBoardGridSize()
        self._blockHeightPx, self._blockWidthPx = self._calculateBlockSize()

        if (self._currBoardState in [self._boardState.init, self._boardState.stopped, self._boardState.paused, self._boardState.ready]):
            #Clear widgets from each layouts
            #self._clearPegBoard()
            #self._clearLayout(self.generalLayout)
            self._houseCleaning()
            self._stats = GaltonBoardResultTracking(self._boardDepth, self._nBalls)
            self._createBoardHeader()        
            self._createPegBoard()
            self._createResultsDisplay()

            # Initialize the bucket values
            self._initBucketValues()
            self._initialize()

            self._currBoardState = self._boardState.ready
            self.timer.start(self._eventTimerInterval, self)
        else:
            print(f'Do nothing for now in board state {self._currBoardState}')

        
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
            if self._ball.getBallState() == self._ballState.init:
                self._setCurrentBallCount(self._ballCtr + 1)
                self.statusBar.showMessage(f'Timer Event | Current State of Ball is Ready')                
                self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  
                self._stats.resetEventList()
                self._ball.setBallState(self._ballState.inProgress)
                # starting timer
                self.timer.start(self._eventTimerInterval, self)
            # INPROGRESS
            elif self._ball.getBallState() == self._ballState.inProgress:
                #Check on position
                #print(f'check: {self._ball.getBallXCoord()} {self._boardVertBlocks - 1}')
                # if the ball is done, reset and start next ball
                if self._ball.getBallXCoord() == self._boardVertBlocks - 1:
                    self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].clear()
                    self._ball.setBallState(self._ballState.inProcess)   
                elif self._ball.getBallCoords() in self._pegCoords:
                    self.statusBar.showMessage(f'Timer Event | Current State of Ball Coords: {self._ball.getBallCoords()}')
                    # move to next coord
                    rndN = self._stats.eventResult()
                    #print (rndN)
                    if rndN < 5:
                        #print("Left")
                        self._stats.updatePathList(rndN)
                        self._ball.setBallCoords((self._ball.getBallXCoord() - 1), (self._ball.getBallYCoord() - 1))
                    else:
                        #print("Right")
                        self._stats.updatePathList(rndN)
                        self._ball.setBallCoords((self._ball.getBallXCoord() - 1), (self._ball.getBallYCoord() + 1))
                    self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  
                    self.statusBar.showMessage(f'Timer Event | Current Stats:  ')                
                else:
                    self.statusBar.showMessage(f'Timer Event | Current State of Ball Coords: {self._ball.getBallXCoord()}, {self._ball.getBallYCoord()}')
                    self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].clear()
                    self._ball.setBallCoords(self._ball.getBallXCoord() + 1, self._ball.getBallYCoord())
                    self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  

                self._messageBox.setText(f'Ball # {self._getCurrentBallCount()} updated path {self._stats.returnPathList()}')
                self.timer.start(self._eventTimerInterval, self)                    

            # INPROCESS
            # process the stats for the ball that just finished
            elif self._ball.getBallState() == self._ballState.inProcess:
                self.statusBar.showMessage(f'Timer Event | Current State of Ball : {self._ball.getBallState()}')
                self._messageBox.setText(f'Ball # {self._getCurrentBallCount()} out of {self._nBalls}')
                # finish if the last ball has been processed
                if self._getCurrentBallCount() != self._nBalls:
                    self._ball.setBallState(self._ballState.init)   
                    self._resetBallPosition()
                else:
                    self._ball.setBallState(self._ballState.lastBall)
                
                # Determine which bucket is being updated
                self._stats.incrementBucketValue(self._stats.getBucketID(), 1)
                self.buckets[self._stats.getBucketID()].setText(f'{self._stats.getBucketValue(self._stats.getBucketID())}')
                
                self.timer.start(self._eventTimerInterval, self)

            # LASTBALL
            elif self._ball.getBallState() == self._ballState.lastBall:
                self.statusBar.showMessage(f'Timer Event | Current State of Ball : {self._ball.getBallState()}')
                self._messageBox.setText(f'Last Ball.....Done')
                self._currBoardState == self._boardState.stopped
                self.timer.stop()
            else:
                self.statusBar.showMessage(f'Timer Event | Current State {self._ball.getBallState()} does not exist.')
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

    def _setEventTimerInterval(self, n):
        self._eventTimerInterval = n
        return
    
    def _getEventTimerInterval(self):
        return self._eventTimerInterval
        
    def _resetBallPosition(self):
        self._ball.setBallCoords(0,floor(self._boardHorBlocks/2))
        return
        
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
        self._inputBoardDepthBox.setFixedWidth((floor(self._boardHorBlocks/3) ) * self._blockWidthPx)
        self._inputBoardDepthBox.setFont(QFont("Arial",15))
        self._inputBoardDepthBox.setReadOnly(True)
        self._inputBoardDepthBox.setText(f'Depth={self._boardDepth}')
        # Add to the general layout
        self._boardHeaderLayout.addWidget(self._inputBoardDepthBox, 1, 0)
        
        # Create Input box to enter the number of balls
        self._inputNumBallsBox = QLineEdit()
            
        # Basic layout params
        self._inputNumBallsBox.setFixedHeight(25)
        self._inputNumBallsBox.setValidator(QIntValidator())
        self._inputNumBallsBox.setAlignment(Qt.AlignHCenter)
        self._inputNumBallsBox.setFixedWidth((floor(self._boardHorBlocks/3) ) * self._blockWidthPx)
        self._inputNumBallsBox.setReadOnly(True)
        self._inputNumBallsBox.setFont(QFont("Arial",15))
        self._inputNumBallsBox.setText(f'#Balls={self._nBalls}')
        # Add to the general layout
        self._boardHeaderLayout.addWidget(self._inputNumBallsBox, 1, 1)

        # Create Input box to enter the number of balls
        self._eventTimerIntervalBox = QLineEdit()
            
        # Basic layout params
        self._eventTimerIntervalBox.setFixedHeight(25)
        self._eventTimerIntervalBox.setValidator(QIntValidator())
        self._eventTimerIntervalBox.setAlignment(Qt.AlignHCenter)
        self._eventTimerIntervalBox.setFixedWidth((floor(self._boardHorBlocks/3)) * self._blockWidthPx)
        self._eventTimerIntervalBox.setReadOnly(True)
        self._eventTimerIntervalBox.setFont(QFont("Arial",15))
        self._eventTimerIntervalBox.setText(f'Timer={self._eventTimerInterval} ms')
        # Add to the general layout
        self._boardHeaderLayout.addWidget(self._eventTimerIntervalBox, 1, 2)

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
                #self.buckets[key].clear()
                if self.buckets[key] is not None:
                    print (f'Removing {self.buckets[key]}')
                    self._bucketLayout.removeWidget(self.buckets[key])    
                self.buckets[key].clear()
    
            self._stats.clearBucketValues()                    
            self._clearBucketCoords()
            self.generalLayout.removeItem(self._bucketLayout)
        
        return
        
    def _clearBucketCoords(self):
        
        if self._bucketContentCoords:
            self._bucketContentCoords = []
        
        for key, _ in self._bucketCoords.items():
            if self.buckets[key] is not None:
                self.buckets.pop(key)
        
        if self._bucketCoords:
            self._bucketCoords = {}

        return
        
    def _createResultsDisplay(self):
        """This display updates the user with the current status of the events."""
        self._bucketLayout = QGridLayout()
        self._bucketCoords = {}
        #self.buckets = []
        #self._bucketContentCoords = []
        self._bucketLayout.setSpacing(self._blockWidthPx)
        
        print(f'{self._boardHorBlocks}')
        print(f'{self._bucketContentCoords}')
        self._bucketContentCoords = [ (self._boardHorBlocks, y) for y in range(self._boardHorBlocks)]
        for x,y in self._bucketContentCoords:
            # calculate and the bucket id as the key - 0, 1, 2 etc
            # to align with the logic for counting R's
            if y%2 == 0:
                self._bucketCoords[floor(y/2)] = (x,y)
          
        # Need to display blank blocks along side the Edit boxes
        for key, coords in self._bucketCoords.items():
            print (f'key = {key}')
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