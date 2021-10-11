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


def main():
    '''
        Process to track events in the Bean Counter
        1. Select depth and number of events
        2. At each level in the triangle, select a random number
        3. Add each event result to a list
        4. Add each list to a dictionary
        5. Plot the results
    '''
    depth = 8
    nSamples = 100
    nTotalLeft = 0
    nTotalRight = 0
    sampleAry = np.empty((0, depth), np.int8)
    eventTotalAry = [0] * (depth + 1)
    #print ("rnd=", np.int8(100.0 * random.random()))
    
    for k in range(100000):
        for j in range(nSamples):
            nEventsLeft = 0
            nEventsRight = 0
            #print("Sample #", j)
            cntR = 0
            evtAry = ['-'] * (depth + 1)
            evtList = []
            for i in range(depth):
                #print ("Event #", i)
                #rndN = np.int8(100.0 * random.random())
                #rndN = random.randint(0, 9)
                #np version
                #rndN = np.random.randint(0, 9 + 1)                
                rndN = _sysrand.randint(0, 9)
                #print (rndN)
                if rndN < 5:
                    #print("Left")
                    evtResult = "L"
                    nEventsLeft += 1
                    nTotalLeft += 1
                else:
                    #print("Right")
                    evtResult = "R"
                    nEventsRight += 1
                    nTotalRight += 1
                    
                evtList.append(evtResult)
                evtAry[i] = evtResult
                #print(evtAry)
            #print (evtList)
            
            # Count the number of Right entries to determine which bucket receives the tally
            cntR = evtAry.count("R")
            #print (cntR)
            eventTotalAry[cntR] += 1
            
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
