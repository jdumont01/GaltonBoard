# 
#   File:   GaltonBoardBall.py
#   Date:   20-Dec-2021
#   Author: Joe Dumont
#

# Imports
from    BallState       import *
 
# Module version
__version__ = '0.9'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

class GaltonBoardBall():
    """Ball class when the Galton Board supports multiple in-play balls."""
    def __init__(self, xValue = 0, yValue = 0, color = '#000000'):
        self._ballState = BallState()
        self._currState = self._ballState.init
        self._currXValue = xValue
        self._currYValule = yValue
        self._color = color                         # Default is black
    # end of __init__
        
    def setBallState(self, state):
        '''
            setBallState (Public):  
                sets the state of the ball
                            
            args:    state:const - one of the constants in the BallState class
            return:  none
        '''
        if state in [self._ballState.init, self._ballState.inProgress, self._ballState.inProcess, self._ballState.complete, self._ballState.lastBall]:
            self._currBallState = state
        else:
            print(f'Ball state {state} is invalid.')
            
        return
    # end of setBallState
        
    def getBallState(self):
        '''
            getBallState (Public):  
                return the state of the ball.
                            
            args:    none
            return:  state:const - one of the constants in the BallState class
        '''

        return self._currBallState
    # end of getBallState
        
    def setBallCoords(self, x, y):
        '''
            setBallCoords (Public):  
                set the x, y position of the ball on the board.
                            
            args:    x:int - x coordinate of the ball
                     y:int - y coordinate of the ball
            return:  none
        '''

        if x >= 0:
            self._ballX = x
        else:
            print(f'x coordinate must be >= 0')
            
        if y>= 0:
            self._ballY = y        
        else:
            print(f'y coordinate must be >= 0')
        
        return
    # end of setBallCoords
    
    def getBallCoords(self):
        '''
            getBallCoords (Public):  
                return the x,y coordinates of the ball.
                            
            args:    none
            return:  x:int - x coordinate of the ball
                     y:int - y coordinate of the ball
        '''
        #print (f'{self._ballX}, {self._ballY}')
        return self._ballX, self._ballY
    # end of getBallCoords
    
    def getBallXCoord(self):
        '''
            getBallXCoord (Public):  
                return the x coordinate of the ball.
                            
            args:    none
            return:  x:int - x coordinate of the ball
        '''
        #print (f'In getBallXCoord: {self._ballX}')
        return self._ballX
    # end of getBallXCoord

    def getBallYCoord(self):
        '''
            getBallYCoord (Public):  
                return the y coordinate of the ball.
                            
            args:    none
            return:  y:int - y coordinate of the ball
        '''
        #print (f'In getBallYCoord: {self._ballY}')
        return self._ballY
    # end of getBallYCoord
    
    def setBallColor(self, color):
        '''
            setBallColor (Public):  
                set the color of the ball.
                            
            args:    color:hex - hex value of the color 
            return:  none
        '''
        self._color = color

        return
    # end of setBallColor
    
    def getBallColor(self):
        '''
            getBallColor (Public):  
                return the color of the ball.
                            
            args:    none
            return:  color:hex - hex value of the color 
        '''
        #print (f'Ball color:  {self._color}')
        
        return self._color
    # end of getBallColor
        
# end of class GaltonBoardBall
    
               
