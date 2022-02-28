# BallState.y 
# Module version

__version__ = '0.1'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

# Use by the Board to determine how to process each ball event
class BallState():
    init = 'INIT'              # ball is ready 
    inProgress = 'INPROGRESS'  # ball is in play on board
    inProcess = 'INPROCESS'    # process of being counted
    complete = 'COMPLETE'      # ball has completed board
    lastBall = 'DONE'          # last ball to be processed
    
