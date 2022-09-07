# 
#   File:   GaltonBoard.py
#   Date:   20-Dec-2021
#   Author: Joe Dumont
#

# Import supporting modules
from BallState                      import *
from BoardState                     import *
from statisticsView                 import *
from GaltonBoardResultTracking      import *
from GaltonBoardBall                import *
from GaltonBoardUi                  import *

# Module version
__version__ = '0.9'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

# Client side code
def main():
    app = QApplication(sys.argv)
    view = GaltonBoardUi(board_depth=3, nBalls = 30)
    view.show()
    sys.exit(app.exec_())

# main method
if __name__ == '__main__':
    main()