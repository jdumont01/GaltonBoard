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

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtCore import Qt

from math import *
import      random

_sysrand = random.SystemRandom()


__version__ = '0.1'
__author__ = 'Joe Dumont'

import random
import sys

class BallState():
    init = 'INIT'              # ball is ready 
    inProgress = 'INPROGRESS'  # ball is in play on board
    inProcess = 'INPROCESS'    # process of being counted
    complete = 'COMPLETE'      # ball has completed board
    
# creating game window
class GaltonBoardUi(QMainWindow):
    """Galton Board Main Window"""
    
    def __init__(self, board_depth = 7, eventTimer = 100, widthP = 800, heightP = 900):
        """View UI Initializer"""
        
        super(GaltonBoardUi, self).__init__()

        self._boardDepth = board_depth
        self._boardWidthPx = widthP
        self._boardHeightPx = heightP
        self._boardHorBlocks, self._boardVertBlocks = self._calculateBoardGridSize()
        self._blockHeightPx, self._blockWidthPx = self._calculateBlockSize()
        self._pegCoords = []
        self._eventTimer = eventTimer
        self.label = {}

        self._ballState = BallState()
        self._currBallState = self._ballState.init
        
        #ball coords
        self._ballX = 0
        self._ballY = floor(self._boardHorBlocks/2)
        
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
        self.statusBar.showMessage(str("Starting"))
        
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
        self._createUserMessageDisplay()
        self._createPegBoard()
        self._createResultsDisplay()
        self._start()

        # starting the board object
        #self.board.start()

        # showing the main window
        self.show()

    def _start(self):
        """Start the board events."""
        
        self.timer.start(Board.SPEED, self)

    # time event method
    def timerEvent(self, event):
  
        # checking timer id
        if event.timerId() == self.timer.timerId():
            self.statusBar.showMessage(f'Timer Event {event} | Current State of Ball {self._currBallState}')
            
            # Ball state types from BallState class
            if self._getBallState() == self._ballState.init:
                self.statusBar.showMessage(f'Timer Event | Current State of Ball is Ready')                
                self.label[self._createKeyFromCoords(self._ballX, self._ballY)].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  
                self._setBallState(self._ballState.inProgress)
                # starting timer
                self.timer.start(Board.SPEED, self)
            
            if self._getBallState() == self._ballState.inProgress:
                if self._getBallCoords() in self._pegCoords:
                    self.statusBar.showMessage(f'Timer Event | Current State of Ball Coords: {self._getBallCoords()}')
                    # move to next coord
                    rndN = _sysrand.randint(0, 9)
                    #print (rndN)
                    if rndN < 5:
                        print("Left")
                        self._setBallCoords(self._ballX - 1, self._ballY - 1)                        
                    else:
                        print("Right")
                        self._setBallCoords(self._ballX + 1, self._ballY - 1)                        
                    self.label[self._createKeyFromCoords(self._ballX, self._ballY)].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  
                    self.timer.start(Board.SPEED, self)

                else:
                    self.statusBar.showMessage(f'Timer Event | Current State of Ball Coords: {self._ballX}, {self._ballY}')
                    self.label[self._createKeyFromCoords(self._ballX, self._ballY)].clear()
                    self._setBallCoords(self._ballX + 1, self._ballY)
                    self.label[self._createKeyFromCoords(self._ballX, self._ballY)].setPixmap(QPixmap("c:\\users\\jdumo\\documents\\filled_circle1600.png"))  
                    self.timer.start(Board.SPEED, self)

            # update the window
            self.update()

    def _setBallState(self, state):
        self._currBallState = state
        
    def _getBallState(self):
        return self._currBallState
        
    def _setBallCoords(self, x, y):
        self._ballX = x
        self._ballY = y
        
        return
    
    def _getBallCoords(self):
        print (f'{self._ballX}, {self._ballY}')
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
        self.display = QLineEdit()
            
        # Basic layout params
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignLeft)
        self.display.setReadOnly(True)

        # Add to the general layout
        self.generalLayout.addWidget(self.display)
        
        return

    def _createPegBoard(self):
        """Creates the Galton Board"""
        pegLayout = QGridLayout()
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
            pegLayout.addWidget(self.label[key], coords[0], coords[1])
                                
        # Add to general layout
        self.generalLayout.addLayout(pegLayout)
        
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
        
    def _createPegBoard2(self):
        """Creates the Galton Board"""
        pegLayout = QGridLayout()
        self.pegCoords = {}
        
        # test
        pegCoords = {
                        '01': (0,0), '11': (0,1), '21': (0,2), '31': (0,3), '41': (0,4),
                        '02': (1,0), '12': (1,1), u"\u2B24": (1,2), '32': (1,3), '42': (1,4),
                        '03': (2,0), '23': (2,1), '23': (2,2), '33': (2,3), '43': (2,4),
                        '04': (3,0), u"\u2B24": (3,1), '24': (3,2), u"\u2B24": (3,3), '44': (3,4)
                    }
        # Calculate grid size based on board depth
        
        # Position pegs using large circle unicode
        for pegText, coord in pegCoords.items():
            self.pegCoords[pegText] = QLabel(pegText)
            self.pegCoords[pegText].setFixedSize(20,20)
            pegLayout.addWidget(self.pegCoords[pegText], coord[0], coord[1])
        # Create vertial buckets
                
        # Add to general layout
        self.generalLayout.addLayout(pegLayout)
        
        return
        
    def _createResultsDisplay(self):
        """This display updates the user with the current status of the events."""
        resDisplayLayout = QGridLayout()
        
        for y in range(0,self._boardHorBlocks, 2):
            display = QLineEdit()            
            # Basic layout params   
            display.setFixedHeight(50)
            display.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            display.setReadOnly(True)
            resDisplayLayout.addWidget(display, 0, y)

        # Add to the general layout
        self.generalLayout.addLayout(resDisplayLayout)

        return
        
    # Public Interfaces
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
    view = GaltonBoardUi(board_depth=4)
    view.show()
    sys.exit(app.exec_())


# main method
if __name__ == '__main__':
    main()