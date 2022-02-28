# GaltonBoardBall.py
 
# Module version
__version__ = '0.9'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

from    BallState       import *

class GaltonBoardBall():
    """Ball class when the Galton Board supports multiple in-play balls."""
    def __init__(self, xValue = 0, yValue = 0, color = '#000000'):
        self._ballState = BallState()
        self._currState = self._ballState.init
        self._currXValue = xValue
        self._currYValule = yValue
        self._color = color                         # Default is black
        
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
        
    def setBallColor(self, color):
        self._color = color
        return
        
    def getBallColor(self):
        #print (f'Ball color:  {self._color}')
        return self._color
    
               
