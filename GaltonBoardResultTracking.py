# GaltonBoardResultTracking
# Module version
__version__ = '0.9'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

from math import *
import      sys
import      random
import      matplotlib.pyplot as plt
import      plotly as pl
import      numpy as np
import      matplotlib
_sysrand = random.SystemRandom()


class GaltonBoardResultTracking():
    """Calculate and display all stats."""
    def __init__(self, numEvents = 7, numSamples = 50):
        self._nEvents = numEvents
        self._nSamples = numSamples
        self._nTotalLeft = 0
        self._nTotalRight = 0
        self._sampleAry = np.empty((0, self._nEvents), np.int8)
        self._eventTotalAry = [0] * (self._nEvents + 1)
        self._nEventsLeft = 0
        self._nEventsRight = 0
        #print("Sample #", j)
        self._cntR = 0
        self._evtAry = ['-'] * (self._nEvents + 1)
        self._evtList = []

    def eventResult(self):
        """method can change the way the randmom number generator works."""
        return _sysrand.randint(0, 9)

    def updatePathList(self, result):
        """result will be """
        if result < 5:
            evtResult = "L"
            self._nEventsLeft += 1
            self._nTotalLeft += 1
        else:
            #print("Right")
            evtResult = "R"
            self._nEventsRight += 1
            self._nTotalRight += 1

        self._evtList.append(evtResult)
        #self._evtAry[i] = evtResult
        #print(evtAry)
        #print (evtList)

        return

    def resetEventList(self):
        self._nEventsLeft = 0
        self._nEventsRight = 0
        self._evtList = []
        
    def getBucketID(self):
        # Count the number of Right entries to determine which bucket receives the tally
        #print (self._cntR)
        self._cntR = self._evtList.count("R")
        
        return self._cntR 

    def clearBucketValues(self):
        self._eventTotalAry = [0] * (self._nEvents + 1)        
        
    def incrementBucketValue(self, bucket, n):
        self._eventTotalAry[bucket] = self._eventTotalAry[bucket] + 1
        
    def getBucketValue(self, bucket):
        return self._eventTotalAry[bucket]
        
    def returnPathList(self):        
        #print (self._evtList)
        return str(self._evtList)
    
    def getResultsArray(self):
        print (f'In getResultsArray: {self._eventTotalAry}')
        return self._eventTotalAry
        
    def getResultsInLists(self):
        
        #for key in range(self._eventTotalAry):
        #print (f'{key}, {self._eventTotalAry[key]}')
        print (f'{self._eventTotalAry}')
        return
