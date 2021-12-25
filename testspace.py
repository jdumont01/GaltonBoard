# BeanCounterSimulator.py

# imports
import      sys
import      matplotlib.pyplot as plt
import      plotly as pl
import      numpy as np
from        mpl_toolkits.mplot3d import axes3d, Axes3D
from        matplotlib.animation import FuncAnimation
import      matplotlib.animation as animation
from        matplotlib import cm
from        matplotlib.ticker import LinearLocator, FormatStrFormatter
import      matplotlib
import      random

_sysrand = random.SystemRandom()

def calcRandom(x):
    return "L" if x < 5 else "R"
    
def main():
    '''
        Process to track events in the Bean Counter
        1. Select depth and number of events
        2. At each level in the triangle, select a random number
        3. Add each event result to a list
        4. Add each list to a dictionary
        5. Plot the results
    '''
    evtList = [x for x in range(10)]
    print(evtList)
    evtList = [_sysrand.randint(0, 9) for i in range(10)]
    print(evtList)
    print (list(map(calcRandom, evtList)))
    return
    
#end of main
 
# *****
# Python entry point
# *****
if __name__ == "__main__":
    main()
    
    print ("Done!")    
