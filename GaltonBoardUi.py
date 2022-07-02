# GaltonBoardUi.py

# Module version
__version__ = '0.9'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import (
    QApplication,           # reason
    QMainWindow,            #
    QWidget,                #
    QFrame,                 #
    QGridLayout,            #
    QLabel,                 #
    QLineEdit,              #
    QPushButton,            #
    QVBoxLayout,            #
    QStatusBar,             #
    QMenuBar,               #
    QMenu,                  #
    QToolBar,               #
    QAction,                #
    QInputDialog,           #
    QMessageBox             #
)

from PyQt5.QtGui import (
    QPainter,               #
    QBrush,                 #
    QPen,                   #
    QPixmap,                #
    QFont,                  #
    QIntValidator,          # Validate integer input from the user
    QDoubleValidator        # Validate float input from the user
)

from PyQt5.QtCore import (
    pyqtSignal,             #
    QBasicTimer,            # 
    QTimer,                 #
    Qt,                     #
    QEvent                  #
)
import math
from BallState                      import *
from BoardState                     import *
from GaltonBoardBall                import *
from GaltonBoardResultTracking      import * 
from statisticsView                 import *


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
        self._expBucketCoords = []
        self._bucketContentCoords = []
        self._bucketExpectationContentCoords = []
        self._eventTimerInterval = eventTimer
        self.label = {}
        self.buckets = {}
        self.expBuckets = {}
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

        # UI characteristics
        self.defaultFontSize = 15
        
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
        self.showStatsView = False 
        self._refreshStatsPeriod = 5000
        self.resultsDisplay = statisticsView(self)

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
        self.showStatsView = not self.showStatsView
        #self.statUiList.append(self.resultsDisplay)
        if self.showStatsView :        
            self.refreshTimer = QTimer()
            self.refreshTimer.start(self._refreshStatsPeriod)       
            self.refreshTimer.timeout.connect(self._refreshStatsView)  
            self.resultsDisplay.displayResultsHistogram(self._stats.getResultsArray())
            self.resultsDisplay.show()
        else:
            self.refreshTimer.stop()
            self.resultsDisplay.closeWindow()
            
        return       

    def _refreshStatsView(self):
        """Call the Views verson of refreshing the stats UI"""
        if self.showStatsView :
            self.refreshTimer.stop()
            self.resultsDisplay.refreshResultsHistogram(self._stats.getResultsArray())
            self.resultsDisplay.show()
            self.refreshTimer.start(self._refreshStatsPeriod)       
            
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
            #del self._stats 
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
                
        return  

    def _restart(self):
        print (f'board state = {self._currBoardState}')
        
        if self._currBoardState == self._boardState.ready:
            #Clear widgets from each layouts
            self._houseCleaning()
            self._createBoardHeader()        
            self._createPegBoard()
            self._createResultsDisplay()
            self._createExpectedResultsDisplay()
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
            self._createExpectedResultsDisplay()
            
            # Initialize the bucket values
            self._initBucketValues()
            self._initExpectationBucketValues()
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

            # Ball state types from BallState class
            # INIT
            if self._ball.getBallState() == self._ballState.init:
                self._setCurrentBallCount(self._ballCtr + 1)
                self.statusBar.showMessage(f'Timer Event | Current State of Ball is Ready')                
                self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].setPixmap(QPixmap(".\\images\\filled_circle1600.png"))  
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
                    if rndN < 5:
                        self._stats.updatePathList(rndN)
                        self._ball.setBallCoords((self._ball.getBallXCoord() - 1), (self._ball.getBallYCoord() - 1))
                    else:
                        self._stats.updatePathList(rndN)
                        self._ball.setBallCoords((self._ball.getBallXCoord() - 1), (self._ball.getBallYCoord() + 1))
                    self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].setPixmap(QPixmap(".\\images\\filled_circle1600.png"))  
                    self.statusBar.showMessage(f'Timer Event | Current Stats:  ')                
                else:
                    self.statusBar.showMessage(f'Timer Event | Current State of Ball Coords: {self._ball.getBallXCoord()}, {self._ball.getBallYCoord()}')
                    self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].clear()
                    self._ball.setBallCoords(self._ball.getBallXCoord() + 1, self._ball.getBallYCoord())
                    self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].setPixmap(QPixmap(".\\images\\filled_circle1600.png"))  

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
        
    def _resizeBoardBasedOnInputs(self):
        """Calculate the fraction factor that will be used to determine how large the   
            board elements are based on the users input."""
    
        print(f'{floor(sqrt((self._boardHeightPx * self._boardWidthPx)/(self._boardHorBlocks * self._boardVertBlocks)))}')
        
        return floor(sqrt((self._boardHeightPx * self._boardWidthPx)/(self._boardHorBlocks * self._boardVertBlocks)))
        
        
    def _calculateBlockSize(self):
        """Size the Galton Board widgets based on depth"""
        # assume square for now
        blockWidth = blockHeight = self._resizeBoardBasedOnInputs()
        
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
        #print(f'In _clearPegBoard')
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
                    self.label[key].setPixmap(QPixmap(".\\images\\filled_circle1600.png"))
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
                self.expBuckets[key].setText(f'0')
    
        return
        
    def _clearResultsDisplay(self):
        #print(f'In _clearResultsDisplay')
        if self._bucketLayout is not None:
            for key, _ in self._bucketCoords.items():
                #print (f'key = {key}')
                #self.buckets[key].clear()
                if self.buckets[key] is not None:
                    #print (f'Removing {self.buckets[key]}')
                    self._bucketLayout.removeWidget(self.buckets[key])    
                self.buckets[key].clear()
    
            #self._stats.clearBucketValues()                    
            self._clearBucketCoords()
            self._clearExpcetationBucketCoords()
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

    def _clearExpcetationBucketCoords(self):
        
        if self._bucketExpectationContentCoords:
            self._bucketExpectationContentCoords = []
        
        for key, _ in self._expBucketCoords.items():
            if self.expBuckets[key] is not None:
                self.expBuckets.pop(key)
        
        if self._expBucketCoords:
            self._expBucketCoords = {}

        return
        
    def _createResultsDisplay(self):
        """This display updates the user with the current status of the events."""
        self._bucketLayout = QGridLayout()
        self._bucketCoords = {}
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
        
    def _createExpectedResultsDisplay(self):
        """This display updates the user with the current status of the events."""
        self._expBucketLayout = QGridLayout()
        self._expBucketCoords = {}
        self._expBucketLayout.setSpacing(self._blockWidthPx)
        
        print(f'{self._boardHorBlocks}')
        print(f'{self._bucketExpectationContentCoords}')
        self._bucketExpectationContentCoords = [ (self._boardHorBlocks, y) for y in range(self._boardHorBlocks)]
        for x,y in self._bucketExpectationContentCoords:
            # calculate and the bucket id as the key - 0, 1, 2 etc
            # to align with the logic for counting R's
            if y%2 == 0:
                self._expBucketCoords[floor(y/2)] = (x,y)
          
        # Need to display blank blocks along side the Edit boxes
        for key, coords in self._expBucketCoords.items():
            print (f'key = {key}')
            self.expBuckets[key] = QLineEdit(self)            
            # Basic layout params   
            self.expBuckets[key].setFixedHeight(50)
            self.expBuckets[key].setFixedWidth(self._blockWidthPx)
            self.expBuckets[key].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.expBuckets[key].setReadOnly(True)
            self.expBuckets[key].setFont(QFont("Arial",15))
            self.expBuckets[key].setContentsMargins(0, 0, 0, 0)
            #self.expBuckets[key].setToolTip(f'Value = {self.buckets[key].text()}')
            #self.expBuckets[key].installEventFilter(self)
            self.expBuckets[key].setStyleSheet("""QLineEdit { background-color: green; color: white }""")

            self._expBucketLayout.addWidget(self.expBuckets[key], coords[0], coords[1])

        # Add to the general layout
        self.generalLayout.addLayout(self._expBucketLayout)

        return
        
    def _initBucketValues(self):
        """This function initializes the values of each bucket."""
        for key, _ in self._bucketCoords.items():
            #print (f'{key}')
            self.buckets[key].setText(f"0")

        return
        
        
    def _initExpectationBucketValues(self):
        """This function initializes the values of each bucket."""
        for key, _ in self._expBucketCoords.items():
            #print (f'{key}')
            expVal = math.floor(self._getNumBalls() * (math.comb(self._getBoardDepth(), key)/(math.pow(2, self._getBoardDepth()))))
            self.expBuckets[key].setText(f'{expVal}')
        
        return
        
        
            
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

