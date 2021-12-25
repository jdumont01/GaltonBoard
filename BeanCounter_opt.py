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
def eventResults(x):
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
    depth = 2
    nSamples = 10000
    nTotalLeft = 0
    nTotalRight = 0
    sampleAry = np.empty((0, depth), np.int8)
    eventTotalAry = [0 for _ in range (depth + 1)]
    #print(eventTotalAry)
    #breakpoint()
    #print ("rnd=", np.int8(100.0 * random.random()))
    
    for j in range(nSamples):
        nEventsLeft = 0
        nEventsRight = 0
        #print("Sample #", j)
        cntR = 0
        evtResult = [_sysrand.randint(0, 9) for i in range(depth)]
        print(evtResult)
        #breakpoint()
        evtResult = list(map(eventResults, evtResult))
        print(evtResult)
        nEventsLeft += evtResult.count("L")
        nTotalLeft += nEventsLeft
        nEventsRight += evtResult.count("R")
        nTotalRight += nEventsRight
        
        #print (cntR)
        eventTotalAry[nEventsRight] += 1
            
    print ("Total Left = ", nTotalLeft)
    print ("Total Right = ", nTotalRight)
    print (eventTotalAry)
    
    return
    
#end of main
 
# *****
# Python entry point
# *****
if __name__ == "__main__":
    main()
    
    print ("Done!")    
