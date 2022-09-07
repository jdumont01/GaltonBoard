# 
#   File:   BoardState.py
#   Date:   20-Dec-2021
#   Author: Joe Dumont
#

# Module version
__version__ = '0.1'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

# Use by the Board to determine how to process each ball event
class BoardState():
    init = 'INIT'               # board is being initialized 
    inProgress = 'INPROGRESS'   # board is being drawn
    paused = 'PAUSED'           # board is paused    
    stopped = 'STOPPED'         # board activity has been stopped
    ready = 'READY'             # board is ready to be used

# end of class BoardState