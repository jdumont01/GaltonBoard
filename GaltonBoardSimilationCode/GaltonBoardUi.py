# 
#   File:   GaltonBoardUi.py
#   Date:   2-Jan-2022
#   Author: Joe Dumont
#

# Module version
__version__ = '0.9'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

# Imports
from PyQt5.QtWidgets import (
    QApplication,           # application-level methods like exit, etc.
    QMainWindow,            # main UI object
    QWidget,                # board object as the central widget
    QGridLayout,            # layout for the individual objects on the board.
    QLabel,                 # labels objects
    QLineEdit,              # line graphics
    QPushButton,            # 
    QVBoxLayout,            # UI grid of vertical objects
    QStatusBar,             # status bar at the bottom of the UI
    QMenuBar,               # 
    QMenu,                  #
    QToolBar,               #
    QAction,                # action tied to menu options
    QInputDialog,           # user input for board depth, events and timer
    QMessageBox             #
)

from PyQt5.QtGui import (
    QPixmap,                # display pegs and ball from a png
    QFont,                  # font types/size
    QIntValidator,          # Validate integer input from the user
    QDoubleValidator        # Validate float input from the user
)

from PyQt5.QtCore import (
    QBasicTimer,            # event timer used for each ball event
    QTimer,                 # refresh timer
    Qt                      # PyQt5 text/object alignment
)
import math
from BallState                      import *
from BoardState                     import *
from GaltonBoardBall                import *
from GaltonBoardResultTracking      import * 
from statisticsView                 import *


class GaltonBoardUi(QMainWindow):
    '''
        class GaltonBoardUi
            Methods and data to orchestrate the user-interface.
    '''
    
    def __init__(self, board_depth = 7, parent=None, eventTimer = 1, nBalls= 5, widthP = 800, heightP = 900, bDebug = True):
        
        super(GaltonBoardUi, self).__init__(parent)
        self._boardState = BoardState()
        self._currBoardState = self._boardState.init
        
        # set consts
        self.DEFAULT_BOARD_DEPTH = 7
        self.DEFAULT_EVENT_TIMER = 100
        self.DEFAULT_NUMBER_OF_BALLS = 100
        self.MIN_BOARD_DEPTH = 2
        self.MAX_BOARD_DEPTH = 10
        self.MAX_NUMBER_OF_BALLS = 1000000000
        self.MIN_NUMBER_OF_BALLS = 1
        self.MIN_EVENT_TIMER = 0                # ms
        self.MAX_EVENT_TIMER = 200              # ms
        
        # Create the Menu
        self._createMenuUI()
        
        # initialize the board-specific data
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

        # Initialize ball state
        self._ballState = BallState()
        self._ball = GaltonBoardBall(xValue = 0, yValue = 0)

        # initialize the size of the board
        self._boardHorBlocks = 0
        self._boardVertBlocks = 0
        self._blockHeightPx = 0 
        self._blockWidthPx = 0
        
        # Get a stats object
        self._stats = GaltonBoardResultTracking(self._boardDepth, self._nBalls)
        
        # creating a timer for each ball event
        self.timer = QBasicTimer()

        # calling showMessage method when signal received by board
        self.statusBar = QStatusBar()
        
        # setting title to the window
        self.setWindowTitle('Galton Board')

        # setting geometry to the window
        self.setFixedSize(self._boardWidthPx, self._boardHeightPx)

        # UI characteristics
        self.defaultFontSize = 15
        
        # track all stats UIs
        self.statUiList = list()

        # adding board as a central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # creating a timer to refresh stats
        self.showStatsView = False 
        self._refreshStatsPeriod = 5000
        self.resultsDisplay = statisticsView(self)

        self._initialize()

        # showing the main window
        self.show()
        
        return
    # end of __init__
    
    def __del__(self):
        '''
            "destructor"
        '''
        self._currBoardState = self._boardState.stopped
        self.timer.stop()
        
        for item in self.statUiList:
            self.statUiList.remove(item)
                  
        return
    # end of __del__
    
    # get/set methods
    def _setCurrentBallCount(self, n):
        self._ballCtr = n
        
        return
    # end of _setCurrentBallCount
        
    def _getCurrentBallCount(self):
        return self._ballCtr
    # end fo _getCurrentBallCount
        
    def _setBoardDepth(self, n):
        self._boardDepth = n
        
        return
    # end of _setBoardDepth

    def _getBoardDepth(self):

        return self._boardDepth
    # end of _getBoardDepth
    
    def _setNumBalls(self, n):
        self._nBalls = n 
        
        return
    # end of _setNumBalls
    
    def _getNumBalls(self):
        return self._nBalls
    # end of _getNumBalls
    
    def _setEventTimerInterval(self, n):
        self._eventTimerInterval = n
    
        return
    # end of _setEventTimerInterval
    
    def _getEventTimerInterval(self):
        return self._eventTimerInterval
    # end of _getEventTimerInterval

    def _initialize(self):
        '''
            _initialize
                Initialize the board.  This is the first state the board will enter
                before the UI starts.
            
            args
            input:  none
            return: none
        '''
        self.statusBar.showMessage(f'Select Board --> Start to start the Galton Board.')
        self._ballCtr = 0
        self._currBallState = self._ballState.init
        self._ball.setBallState(self._ballState.init)

        #ball coords
        self._ball.setBallCoords(0, floor(self._boardHorBlocks/2))

        return  
    # end of _initialize
    
    def _configureStatusBar(self):
        '''
            _configureStatusBar
                Configures the status bar UI.
            
            args
            input:  none
            return: none
        '''
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("border : 2px solid black;")
        self.statusBar.showMessage(f'Starting')
        
        return
    # end of _configureStatusBar
        
    def _createMenuUI(self):
        '''
            _createMenuUI
                wrapper function to create the menu bar at the top of the UI.
                    
            args
            input:  none
            return: none
        '''
        self._createMenuActions()
        self._createMenuBar()
        self._connectMenuActions()

        return
    # end of _createMenuUI
    
    def _createMenuBar(self):
        '''
            _createMenuBar
                Creates the text and the shortcuts for the main menu options.
            
            args
            input:  none
            return: none
        '''
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        # Board menu options
        boardMenu = menuBar.addMenu("&Board")
        boardMenu.addAction(self.startAction)
        boardMenu.addAction(self.stopAction)
        boardMenu.addAction(self.resetAction)
        boardMenu.addSeparator()        
        boardMenu.addAction(self.pauseAction)
        boardMenu.addAction(self.resumeAction)
        boardMenu.addSeparator()
        boardMenu.addAction(self.exitAction)

        # Statistics menu options
        statisticsMenu = menuBar.addMenu("&Statistics")        
        statisticsMenu.addAction(self.showStatisticsViewAction)

        # Help menu options
        helpMenu = menuBar.addMenu("&Help")        
        # The following will be added and implemented in a later version
        #helpMenu.addAction(self.helpContentAction)
        #helpMenu.addSeparator()
        helpMenu.addAction(self.startAboutContent)
        
        # Getting Started menu options
        gettingStartMenu = menuBar.addMenu("&Getting Started")
        gettingStartMenu.addAction(self.gettingStartedAction)
        
        return
    # end of _createMenuBar

    def _createMenuActions(self):
        '''
            _createMenuUI
                Create the functional hotkeys and second-level menu options.
                    
            args
            input:  none
            return: none
'''
        # Board menu actions
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
        
        # Statistics menu actions
        self.showStatisticsViewAction = QAction("Res&ults", self)
        self.showStatisticsViewAction.setShortcut("Ctrl+U")

        # Help menu actions
        # The Help content will be implemented at a later date
        #self.helpContentAction = QAction("&Help Content", self)
        #self.helpContentAction.setShortcut("Ctrl+H")
        self.startAboutContent = QAction("&About", self)
        self.startAboutContent.setShortcut("Ctrl+A")

        # Getting Started menu actions
        self.gettingStartedAction = QAction("&Getting Started", self)
        self.gettingStartedAction.setShortcut("Ctrl+G")
                
        return
    # end of _connectMenuActions
           
    def _connectMenuActions(self):
        '''
            _connectMenuActions
                Assigns the logic to each menu action.
                
            args
            input:  none
            return: none
        '''
        # Board Menu Options
        self.startAction.triggered.connect(self._startBoard)
        self.stopAction.triggered.connect(self._stopBoard)
        self.resetAction.triggered.connect(self._resetBoard)
        self.pauseAction.triggered.connect(self._pauseBoard)
        self.resumeAction.triggered.connect(self._resumeBoard)
        self.exitAction.triggered.connect(self._exitBoard)
        
        # Statistics Menu Options
        self.showStatisticsViewAction.triggered.connect(self._createResultsView)
        
        # Help Menu Options
        self.startAboutContent.triggered.connect(self._startAbout)

        # Getting Started 
        self.gettingStartedAction.triggered.connect(self._gettingStarted)

        return
    # end of _connectMenuActions
        
    def _gettingStarted(self):
        '''
            _gettingStarted
                Setup the UI for the Getting Started menu option.
            
            args
            input:  none
            return: none
        '''
        s = f'Getting Stared with the Galton Board simulator.'
        s += f'\n\nMenu Options: '
        s += f'\nBoard - Start, stop, pause and resume a simulation'
        s += f'\nStatistics - Generates a pop out window showing the accumulated number of balls in each bucket in real time.  It is updated every 5 seconds.'
        s += f'\nHelp - Shows the About screen with details pertaining to the state of the program code.'
        s += f'\n\nStart Simulation: '
        s += f'\nTo start a simulation the user will navigate to the Board menu and select Start.'
        s += f'\nThe user will be required to input: '
        s += f'\n\tthe depth of the board (min = 1, max = 10, default = 7)'
        s += f'\n\tthe number of balls to traverse the board (min = 1, max = 1000000000, default = 100)'
        s += f'\n\tthe interval timer (ms) between starting a ball (min = 0, max = 200, default = 100).'
        s += f'\n\t   A timer value of 0 will cause the simulator to go as fast as possible.'
        s += f'\n\nViewing Results:'
        s += f'\nThe user can view the path taken by the ball at the top of the main screen.'
        s += f'\nAt the bottom of the main screen, there are 2 rows of output.'
        s += f'\nThe top row is the accumulated number of balls in a bucket.'
        s += f'\nThe bottom row (green) is the expected number of balls for each bucket.'
        s += f'\nThe expectation value is based on the number of balls defined by'
        s += f'\nthe user, the depth of the board and the index of the bucket.'
        msg = QMessageBox()
        
        msg.setWindowTitle("Getting Started")
        msg.setIcon(QMessageBox.Information)        
        #msg.setInformativeText("Info text")
        #msg.setDetailedText("details")
        msg.setText(s) 
        #msg.setStandardButtons(QMessageBox.Ok)
        
        retV = msg.exec()
        
        return
    # end of _gettingStarted
    
    def _createResultsView(self):
        '''
            _createResultsView
                Logic associated with creating the Stats UI.
            
            args
            input:  none
            return: none
        '''
        self.showStatsView = not self.showStatsView
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
    # end of _createResultsView

    def _refreshStatsView(self):
        '''
            _refreshStatsView
                Call the Views verson of refreshing the stats UI
            
            args
            input:  none
            return: none
        '''
        if self.showStatsView :
            self.refreshTimer.stop()
            self.resultsDisplay.refreshResultsHistogram(self._stats.getResultsArray())
            self.resultsDisplay.show()
            self.refreshTimer.start(self._refreshStatsPeriod)       
            
        return
    # end of _refreshStatsView

    def _startAbout(self):
        '''
            _startAbout
                Logic assoicated with the About action.
            
            args
            input:  none
            return: none
        '''
        s = f'Galton Board Version:  {__version__}\nAuthor:  {__author__}\nReleased:  {__releaseDate__}\nPython Version:  {sys.version}\nVersion Info:  {sys.version_info}'
        QMessageBox.about(self, "About Galton Board", s) 
        #msg.setIcon(QMessageBox.Information)
        #msg.setStandardButtons(QMessageBox.Ok)
        
        return
    # end of _startAbout

    def _startBoard(self):
        '''
            _startBoard
                Logic to get the user input and create the board.
            
            args
            input:  none
            return: none
        '''
        #print (f'In _startBoard; board state = {self._currBoardState}')

        num = self.MIN_BOARD_DEPTH - 1
        ok = False
        
        # Board Depth
        while num < self.MIN_BOARD_DEPTH and ok == False:          
            num, ok = QInputDialog.getInt(self, "Board Depth Dialog", f'Enter the Board Depth\n(Values:  {self.MIN_BOARD_DEPTH} to {self.MAX_BOARD_DEPTH})', self.DEFAULT_BOARD_DEPTH)

            if ok == True and (num >= self.MIN_BOARD_DEPTH and num <= self.MAX_BOARD_DEPTH):
                self._setBoardDepth(num)
                #self._inputBoardDepthBox.setText(f'Depth = {self._getBoardDepth()}')
                break
            else:
                self.statusBar.showMessage(f'Invalid Board Depth Input')
                num = self.MIN_BOARD_DEPTH - 1
                ok = False
        # end while

        # Number of Balls
        num = self.MIN_NUMBER_OF_BALLS - 1
        ok = False

        while num < self.MIN_BOARD_DEPTH and ok == False:                      
            num, ok = QInputDialog.getInt(self, "Number of Tests Dialog", f'Enter the Number of Balls\n(Values:  {self.MIN_NUMBER_OF_BALLS} to {self.MAX_NUMBER_OF_BALLS})', self.DEFAULT_NUMBER_OF_BALLS)

            if ok == True and (num >= self.MIN_NUMBER_OF_BALLS and num <= self.MAX_NUMBER_OF_BALLS):
                self._setNumBalls(num)
                #self._inputNumBallsBox.se.reatText(f'Depth = {self._getNumBalls()}')
                break
            else:
                self.statusBar.showMessage(f'Invalid Ball Number Input')       
                num = self.MIN_NUMBER_OF_BALLS - 1
                ok = False
        # end while

        # Event timer
        num = self.MIN_EVENT_TIMER - 1
        ok = False
        
        while num < self.MIN_BOARD_DEPTH and ok == False:                  
            num, ok = QInputDialog.getInt(self, "Set Event Timer", f'Set Event Timer (ms)\n(Values:  {self.MIN_EVENT_TIMER} to {self.MAX_EVENT_TIMER})', self.DEFAULT_EVENT_TIMER)

            if ok == True and (num >= self.MIN_EVENT_TIMER and num <= self.MAX_EVENT_TIMER):
                self._setEventTimerInterval(num)
                #self._inputNumBallsBox.se.reatText(f'Depth = {self._getNumBalls()}')
                break
            else:
                self.statusBar.showMessage(f'Invalid Time Input')
                num = self.MIN_EVENT_TIMER - 1
                ok = False
        # end while
        
        # reset board state
        if (self._currBoardState in [self._boardState.stopped, self._boardState.paused, self._boardState.ready]):
            self._currBoardState = self._boardState.stopped
        else:
            self._currBoardState = self._boardState.init
        
        self._start()

        return
    # end of _startBoard
        
    def _houseCleaning(self):
        '''
            _houseCleaning
                Wrapper to remove UI components so that the board can be rebuilt when
                the user selects Ctrl-S to restart the simulation.
            
            args
            input:  none
            return: none
        '''
        if (self._currBoardState in [self._boardState.stopped, self._boardState.inProgress, self._boardState.ready]):
            #Clear widgets from each layouts
            self._clearResultsDisplay()
            self._clearPegBoard()
            self._clearLayout(self.generalLayout)
            #del self._stats 
        else:
            print(f'Do nothing for now for Board State {self._currBoardState}')
            
        return
    # end of _houseCleaning
   
    def _stopBoard(self):
        '''
            _stopBoard
                Logic to stop the board processing.
            
            args
            input:  none
            return: none
        '''
        #print (f'In _stopBoard')
        self._messageBox.setText(f'Stopping.....Will implement saving results later.')
        self._currBoardState = self._boardState.stopped
        #self._houseCleaning()
        self.timer.stop()

        return
    # end of _stopBoard
        
    def _resetBoard(self):
        '''
            _resetBoard
                Resets the board stats and accumulated data.
            
            args
            input:  none
            return: none
        '''
        #print (f'In _resetBoard: board state = {self._currBoardState}')
        if (self._currBoardState in [self._boardState.stopped, self._boardState.ready]):
            self._messageBox.setText(f'Resetting Board Statistics.')
            self.timer.stop()
            self._houseCleaning()
            self._start()
        else:
            print(f'In _resetBoard:  invalid board state to reset - {self._currBoardState}')  

        return
    # end of _resetBoard
        
    def _pauseBoard(self):
        '''
            _pauseBoard
                Logic to stop processing without resetting the board.
            
            args
            input:  none
            return: none
        '''
        #print (f'In _pauseBoard')
        self._currBoardState = self._boardState.paused
        self.timer.stop()

        return
    # end of _pauseBoard

    def _resumeBoard(self):
        '''
            _resumeBoard
                The board will continue processing from the last pause state without resetting
                stats.
            
            args
            input:  none
            return: none
        '''
        #print (f'In _resumeBoard')
        if (self._currBoardState in [self._boardState.stopped, self._boardState.paused]):
            self._currBoardState = self._boardState.ready
            self.timer.start(self._eventTimerInterval, self)

        return
    # end of _resumeBoard

    def _exitBoard(self):
        '''
            _exitBoard
                Stops all processing and exits the UI.
            
            args
            input:  none
            return: none
        '''
        #print (f'In _exitBoard')
        self._currBoardState = self._boardState.stopped
        self.timer.stop()
        self.close()
    
        return
    # end of _exitBoard
        
    def _helpContent(self):
        '''
            _helpContent
                UNUSED function - will be implemented in the next version.
            
            args
            input:  none
            return: none
        '''
        #print (f'In _helpContent')

        return
    # end of _helpContent
        
    def _restart(self):
        '''
            _restart
                Resets the board UI and stats.  The board will be redrawn with the new 
                user-defined parameters.
            
            args
            input:  none
            return: none
        '''
        #print (f'board state = {self._currBoardState}')
        
        if self._currBoardState == self._boardState.ready:
            #Clear widgets from each layouts
            self._houseCleaning()
            self._createBoardHeader()        
            self._createPegBoard()
            self._createResultsDisplay()
            self._createExpectedResultsDisplay()
            self._stats = GaltonBoardResultTracking(self._boardDepth, self._nBalls)

        return
    # end of _restart
        
    def _start(self):
        '''
            _start
                Creates the board.
            
            args
            input:  none
            return: none
        '''
        #print (f'In _start; board state = {self._currBoardState}')
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
    # end of _start

    def _processBallInInit(self):
        '''
            _processBallInInit
                Logic asrsociated with preparing a ball to be released into the board.
            
            args
            input:  none
            return: none
        '''
        # start the ball counter
        self._setCurrentBallCount(self._ballCtr + 1)

        # display the event
        self.statusBar.showMessage(f'Timer Event | Current State of Ball is Ready')                

        # place the ball at the entrance to the board
        self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].setPixmap(QPixmap(".\\images\\filled_circle1600.png"))  

        # clear all stats for the current ball
        self._stats.resetEventList()

        # set the ball state 
        self._ball.setBallState(self._ballState.inProgress)

        # starting timer
        self.timer.start(self._eventTimerInterval, self)               

        return
    # end of _processBallInInit

    def _processBallInProgress(self):
        '''
            _processBallInProgress
                Logic to determine how to process the ball when it is either:
                    in play and not in contact with a peg
                    in play and in contact with a peg
                    completed the board traversal
            
            args
            input:  none
            return: none
        '''
        #print(f'check: {self._ball.getBallXCoord()} {self._boardVertBlocks - 1}')
        # IF block:
        #   Check on position to determine how to process the current ball
        # BALL has completed the board and is ready for data processing in the landing bucket
        if self._ball.getBallXCoord() == self._boardVertBlocks - 1:
            self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].clear()
            self._ball.setBallState(self._ballState.inProcess)   
        # BALL is in play in the board AND it contacts a peg
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
        # BALL is in play in the board AND it does not contact a peg
        else:
            self.statusBar.showMessage(f'Timer Event | Current State of Ball Coords: {self._ball.getBallXCoord()}, {self._ball.getBallYCoord()}')
            self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].clear()
            self._ball.setBallCoords(self._ball.getBallXCoord() + 1, self._ball.getBallYCoord())
            self.label[self._createKeyFromCoords(self._ball.getBallXCoord(), self._ball.getBallYCoord())].setPixmap(QPixmap(".\\images\\filled_circle1600.png"))  

        # update the user with the updated ball path results
        self._messageBox.setText(f'Ball # {self._getCurrentBallCount()} updated path {self._stats.getPathList()}')
        
        # restart the timer
        self.timer.start(self._eventTimerInterval, self)                    

        return
    # end of _processBallInProgress 

    def _processBallInProcess(self):
        '''
            _processBallInProcess
                Logic to process the ball when it reaches a bucket based on the 
                ball's number.  If it is the last ball then set the state that way
                to complete the simulation.
            
            args
            input:  none
            return: none
        '''
        # update the user
        self.statusBar.showMessage(f'Timer Event | Current State of Ball : {self._ball.getBallState()}')
        self._messageBox.setText(f'Ball # {self._getCurrentBallCount()} out of {self._nBalls}')

        # IF block
        #   either prepare for the next ball or prepare the board to release
        #   the last ball in the simulation
        if self._getCurrentBallCount() != self._nBalls:
            self._ball.setBallState(self._ballState.init)   
            self._resetBallPosition()
        else:
            self._ball.setBallState(self._ballState.lastBall)
        
        # Determine which bucket is being updated
        self._stats.incrementBucketValue(self._stats.getBucketID())
        self.buckets[self._stats.getBucketID()].setText(f'{self._stats.getBucketValue(self._stats.getBucketID())}')
        
        # restart the timer 
        self.timer.start(self._eventTimerInterval, self)

        return
    # end of _processBallInProcess

    def _processLastBall(self):
        '''
            _processLastBall
                Notify the board to stop processing on this event cycle since the
                last ball was processed in the previous event.
            
            args
            input:  none
            return: none
        '''
        # update the user
        self.statusBar.showMessage(f'Timer Event | Current State of Ball : {self._ball.getBallState()}')
        self._messageBox.setText(f'Last Ball.....Done')

        # reset the board state
        self._currBoardState == self._boardState.stopped

        # stop the ball timer
        self.timer.stop()
    
        return
    # end of _processLastBall

    def timerEvent(self, event):
        '''
            timerEvent (Private)
                Logic to determine how the ball will respond during the next 
                timer clock cycle.  This is based on the state of the ball.
                The ball state types from BallState class.

            args   
            input:  event:timer object - contains timer id
            return: none
        '''
  
        # checking timer id
        if event.timerId() == self.timer.timerId():
            self.statusBar.showMessage(f'Timer Event {event} | Current State of Ball {self._currBallState}')

            # INIT
            if self._ball.getBallState() == self._ballState.init:
                self._processBallInInit()
            # INPROGRESS
            elif self._ball.getBallState() == self._ballState.inProgress:
                self._processBallInProgress()
            # INPROCESS
            # process the stats for the ball that just finished
            elif self._ball.getBallState() == self._ballState.inProcess:
                self._processBallInProcess()
            # LASTBALL
            elif self._ball.getBallState() == self._ballState.lastBall:
                self._processLastBall()
            # INVALID STATE
            else:
                self.statusBar.showMessage(f'Timer Event | Current State {self._ball.getBallState()} does not exist.')
            # update the window
            self.update()

        return
    # end of timerEvent

    def _clearLayout(self, layout):
        '''
            _clearLayout
                Remove widgets from layout.
            
            args
            input:  none
            return: none
        '''
        
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    layout.removeWidget(widget)
                    #widget.setParent(None)
                else:
                    self._clearLayout(item.layout())        
        
        return
    # end of _clearLayout

    def _clearWidgetsFromLayout(self, layout):
        '''
            _clearWidgetsFromLayout
                remove widget objects from the UI.
            
            args
            input:  none
            return: none
        '''
        for j in reversed(range(layout.count())): 
            #print (f'{j}')
            widgetToRemove = layout_item.itemAt(j).widget()
            
            if widgetToRemove is not None:
                # remove it from the layout list
                layout_item.removeWidget(widgetToRemove)
                # remove it from the gui
                widgetToRemove.setParent(None)
                    
        return
    # end of _clearWidgetsFromLayout
            
    def _resetBallPosition(self):
        '''
            _resetBallPosition
                sets the ball position to be the top of the
                board prior to being released.
                
            args
            input:  none
            return: none
        '''
        self._ball.setBallCoords(0,floor(self._boardHorBlocks/2))
        return
    # end of _resetBallPosition
    
    def _calculateBoardGridSize(self):
        '''
            _calculateBoardGridSize
                Determine how many grid elements are needed based on Board depth.
                
            args
            input:  none
            return: nHorizontalBlocks:int - number of blocks along the x-axies
                    nVerticalBlocks:int - number of blocks alongs the y-axis
        '''
        nHorizontalBlocks = 2 * self._boardDepth + 1
        nVerticalBlocks = 2 * self._boardDepth + 2
        
        return nHorizontalBlocks, nVerticalBlocks
    # end of _calculateBoardGridSize
        
    def _resizeBoardBasedOnInputs(self):
        '''
            _resizeBoardBasedOnInputs
            Calculate the fraction factor that will be used to determine how large the   
            board elements are based on the users input.
            
            args
            input:  none
            return: none
        '''
    
        print(f'{floor(sqrt((self._boardHeightPx * self._boardWidthPx)/(self._boardHorBlocks * self._boardVertBlocks)))}')
        
        return floor(sqrt((self._boardHeightPx * self._boardWidthPx)/(self._boardHorBlocks * self._boardVertBlocks)))
    # end of _resizeBoardBasedOnInputs
        
    def _calculateBlockSize(self):
        '''
            _calculateBlockSize
                Determine the size of the blocks based on the user input defining the board 
                dimensions.
                
            args
            input:  none    
            return: blockWidth:int - size of the block in the y-direction
                    blockHeight:int - sizd of the block in the x-direction
        '''
        blockWidth = blockHeight = self._resizeBoardBasedOnInputs()
        
        return blockWidth, blockHeight
    # end of _calculateBlockSize
    
    def _createUserMessageDisplay(self):
        '''
            _createUserMessageDisplay
                This display updates the user with the current status of the events.

            args
            input:  none
            return: none
        '''
        self._messageBox = QLineEdit()
            
        # Basic layout params
        self._messageBox.setFixedHeight(25)
        self._messageBox.setAlignment(Qt.AlignLeft)
        self._messageBox.setReadOnly(True)
        self._messageBox.setFont(QFont("Arial",15))

        # Add to the header layout
        self._boardHeaderLayout.addWidget(self._messageBox, 0, 0)

        return
    # end of _createUserMessageDisplay

    def _createBoardHeader(self):   
        '''
            _createBoardHeader
                Configures the data displayed at the top of the board:
                    Board Depth
                    Number of Balls
                    Event Timer (ms)
                    
            args    
            input:  none
            return: none
        '''
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
        
        return
    # end of _createBoardHeader
                
    def _clearPegBoard(self):
        '''
            _clearPegBoard
                Clear the objects from the board section of the UI.
                
            args
            input:  none
            return: none
        '''
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
    # end of _clearPegBoard
    
    def _createPegBoard(self):
        '''
            _createPegBoard
                Creates and places the pegs on the board.
                The board geometry is 
                    x = block row number
                    y = block column 
                The board is created by placing blocks, proprotionally sized based on the 
                depth of the board, in the UI.  The blocks will either contain a figure (png
                format) or nothing.  
                
            args
            input:  none
            return: none
        '''
        self._pegLayout = QGridLayout()
        self.pegCoords = {}
        
        # setup the coordinates for each block in the board.
        boardContentCoords = [(x,y) for x in range (self._boardVertBlocks) for y in range(self._boardHorBlocks)]
        for x, y in boardContentCoords:
            self.pegCoords[self._createKeyFromCoords(x,y)] = (x,y)
            
        #print (self.pegCoords)
            
        # determine which blocks will contain a peg
        self._setPegCoords()
        #print (self._pegCoords)
                
        # Create first and list rows' figures
        for key, coords in self.pegCoords.items():
            #print (coords)
            self.label[key] = QLabel(self)
            # draw horizontal lines defining the top of the board where the ball enters
            if coords[0] == 0:
                if coords[1] != floor(self._boardHorBlocks/2):
                    self.label[key].setPixmap(QPixmap(".\\images\\horizontal-line.png"))
                    self.label[key].setAlignment(Qt.AlignLeft)
            # draw vertical lines separating the buckets
            elif coords[0] == self._boardVertBlocks - 1:
                if coords[1] % 2 == 1:
                    self.label[key].setPixmap(QPixmap(".\\images\\vertical_line.png"))
                    self.label[key].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # drag the pegs
            else:
                if coords in self._pegCoords:
                    #print (f'[{x}, {y}]')
                    self.label[key].setPixmap(QPixmap(".\\images\\filled_circle1600.png"))
                    self.label[key].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    
            # resize the objects based on the depth of the board 
            self.label[key].setFixedSize(self._blockWidthPx, self._blockHeightPx)
            self.label[key].setScaledContents(True)
            self.label[key].setContentsMargins(0, 0, 0, 0)
            self._pegLayout.addWidget(self.label[key], coords[0], coords[1])
                                
        # Add to general layout
        self.generalLayout.addLayout(self._pegLayout)
        
        return
    # end of _createPegBoard
    
    def _createKeyFromCoords(self, x, y):
        '''
            _createKeyFromCoords
                Creates a unique dict key to build the blocks on the board UI, 
                based on the coordinates
                
            args    
            input:  x:int - x value
                    y:int - y value
            return: string of the form x<num>y<num> Ex:  x3y4
        '''
        return f'x{x}y{y}'
    # end of _createKeyFromCoords
        
    def _setPegCoords(self):
        '''
            _setPegCoords
                Calcualtes the coordinates for each peg.
            
            args
            input:  none
            return: none
        '''
        for i in range(self._boardVertBlocks):
            if i%2 == 0:
                for j in range(0, (floor(i/2))):
                    p = self._boardDepth - (floor(i/2)) + 1 + (2 * j)
                    self._pegCoords.append((i, p))
                        
        return
    # end of _setPegCoords
        
    def _clearPegCoords(self):
        '''
            _clearPegCoords
                clear the peg coordinate list
            
            args
            input:  none
            return: none
        '''
        self._pegCoords = []
        
        return
    # end of _clearPegCoords
        
    def _clearResultsData(self):
        '''
            _clearResultsData
                Clear the data in the result buckets
                
            args
            input:  none
            return: none
        '''
        if self._bucketLayout is not None:
            for key, _ in self._bucketCoords.items():
                #print (f'key = {key}')
                self.buckets[key].setText(f'0')
                self.expBuckets[key].setText(f'0')
    
        return
    #end of _clearResultsData
        
    def _clearResultsDisplay(self):
        '''
            _clearResultsDisplay
                Remove the bucket objects.
                
            args
            input:  none
            return: none
        '''
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
    # end of _clearResultsDisplay
        
    def _clearBucketCoords(self):
        '''
            _clearBucketCoords
                Reset the coordinates of the buckets
                
            args
            input:  none
            return: none
        '''
        if self._bucketContentCoords:
            self._bucketContentCoords = []
        
        for key, _ in self._bucketCoords.items():
            if self.buckets[key] is not None:
                self.buckets.pop(key)
        
        if self._bucketCoords:
            self._bucketCoords = {}

        return
    # end of _clearBucketCoords

    def _clearExpcetationBucketCoords(self):
        '''
            _clearExpcetationBucketCoords
                Remove the objects for the objects displaying the expected  
                values for each bucket.
                
            args
            input:  none
            return: none
        '''
        if self._bucketExpectationContentCoords:
            self._bucketExpectationContentCoords = []
        
        for key, _ in self._expBucketCoords.items():
            if self.expBuckets[key] is not None:
                self.expBuckets.pop(key)
        
        if self._expBucketCoords:
            self._expBucketCoords = {}

        return
    # end of _clearExpcetationBucketCoords
        
    def _createResultsDisplay(self):
        '''
            _createResultsDisplay
                This display updates the user with the current status of the events.
                
            args
            input:  none
            return: none
        '''
        self._bucketLayout = QGridLayout()
        self._bucketCoords = {}
        self._bucketLayout.setSpacing(self._blockWidthPx)
        
        #print(f'{self._boardHorBlocks}')
        #print(f'{self._bucketContentCoords}')
        self._bucketContentCoords = [ (self._boardHorBlocks, y) for y in range(self._boardHorBlocks)]

        # FOR block:
        #   calculate and the bucket id as the key - 0, 1, 2 etc
        #   to align with the logic for counting R's
        for x,y in self._bucketContentCoords:
            if y%2 == 0:
                self._bucketCoords[floor(y/2)] = (x,y)
          
        # FOR block:
        #   Need to display blank blocks along side the Edit boxes
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
    # end of _createResultsDisplay
    
    def _createExpectedResultsDisplay(self):
        '''
            _createExpectedResultsDisplay
                This display updates the user with the current status of the events.
                
            args
            input:  none
            return: none
        '''
        self._expBucketLayout = QGridLayout()
        self._expBucketCoords = {}
        self._expBucketLayout.setSpacing(self._blockWidthPx)
        
        #print(f'{self._boardHorBlocks}')
        #print(f'{self._bucketExpectationContentCoords}')
        self._bucketExpectationContentCoords = [ (self._boardHorBlocks, y) for y in range(self._boardHorBlocks)]
        # calculate and the bucket id as the key - 0, 1, 2 etc
        # to align with the logic for counting R's
        for x,y in self._bucketExpectationContentCoords:
            if y%2 == 0:
                self._expBucketCoords[floor(y/2)] = (x,y)
          
        # FOR block:
        #   Need to display blank blocks along side the Edit boxes
        for key, coords in self._expBucketCoords.items():
            #print (f'key = {key}')
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
    # end of _createExpectedResultsDisplay
    
    def _initBucketValues(self):
        '''
            _initBucketValues
                This function initializes the values of each bucket.
            
            args
            input:  none
            return: none
        '''
        for key, _ in self._bucketCoords.items():
            #print (f'{key}')
            self.buckets[key].setText(f"0")

        return
    # end of _initBucketValues
        
    def _initExpectationBucketValues(self):
        '''
            _initExpectationBucketValues
                This function initializes the values of each bucket.
                
            args
            input:  none
            return: none
        '''
        for key, _ in self._expBucketCoords.items():
            #print (f'{key}')
            expVal = math.floor(self._getNumBalls() * (math.comb(self._getBoardDepth(), key)/(math.pow(2, self._getBoardDepth()))))
            self.expBuckets[key].setText(f'{expVal}')
        
        return
    # end of _initExpectationBucketValues
        
# end of class GaltonBoardUi            
