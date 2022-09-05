# 
#   File:   GaltonBoardResultTracking.py
#   Date:   20-Dec-2021
#   Author: Joe Dumont
#

# Module version
__version__ = '0.9'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

# Imports
from math import *
import      sys
import      random
import      matplotlib.pyplot as plt
import      plotly as pl
import      numpy as np
import      matplotlib
_sysrand = random.SystemRandom()


class GaltonBoardResultTracking():
    '''
        class GaltonBoardResultTracking
            Calculate and display all stats.
            
    '''
    def __init__(self, numEvents = 7, numSamples = 50):
        '''
            __init__
        '''
        self._nEvents = numEvents   # number of events the ball will complete (= board depth)
        self._nSamples = numSamples # number of balls to be used in the sumulation.

        # intialize counters
        self._nTotalLeft = 0        # number of times the ball fell to the left for all balls
        self._nTotalRight = 0       # number of times the ball fell to the right for all balls
        self._nEventsLeft = 0       # number of times the current ball fell to the left
        self._nEventsRight = 0      # number of times the current ball fell to the right
        self._cntR = 0


        self._evtList = []          # list containing the results of the events at each peg.
        
        # maintain the accumulated values for each bucket
        self._eventTotalAry = [0] * (self._nEvents + 1)

    # end of __init__
    
    def eventResult(self):
        '''
            eventResult (Public):  
                This method can change the way the randmom number generator works.
                In the future multiple randomization functions will be included to compare results.
                            
            args:    none
            return:  randint:int - random number between 0 and 9 inclusive
        '''

        return _sysrand.randint(0, 9)
    # end of eventResult

    def updatePathList(self, result):
        '''
            updatePathList (Public):  
                Update the following counters with the result of the most recent ball event (left or right):
                    _nEventsLeft    number of times the current ball fell to the left 
                    _nEventsRight   number of times the current ball fell to the right 
                    _nTotalLeft     number of times the ball fell to the left for all balls
                    _nTotalRight    number of times the ball fell to the right for all balls
                    
                If the result is 0 - 4, then the ball is going to the left; otherwise it goes to the right.
                            
            args:    result:int - 
            return:  randint:int - random number between 1 and 9 inclusive
        '''
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

        return
    # end of updatePathList

    def resetEventList(self):
        '''
            resetEventList (Public):  
                Resets the event list and the counters for the current ball.
                            
            args:    none
            return:  none
        '''
        self._nEventsLeft = 0
        self._nEventsRight = 0
        self._evtList = []

        return
    # end of resetEventList
    
    def getBucketID(self):
        '''
            getBucketID (Public):  
                Return the results bucket id by returning the number of R events in the 
                current ball path.  0 R = position 0, 1 R = position 1, etc
                
            args:    none
            return:  _cntR:int - The index of the bucket.
        '''
        #print (self._cntR)
        self._cntR = self._evtList.count("R")
        
        return self._cntR 
    # end of getBucketID

    def clearBucketValues(self):
        '''
            clearBucketValues (Public):  
                reset the bucket values upon a board restart, or a new simulation
                
            args:    none
            return:  none
        '''
        self._eventTotalAry = [0] * (self._nEvents + 1)        
        
        return
    # end of clearBucketValues
        
    def incrementBucketValue(self, bucket):
        '''
            incrementBucketValue (Public):  
                Increments the counter for bucketId = bucket
                
            args:    bucket:int - the id of the counter to be updated
            return:  none
        '''
        self._eventTotalAry[bucket] = self._eventTotalAry[bucket] + 1
        
        return
    # end of incrementBucketValue
        
    def getBucketValue(self, bucket):
        '''
            gettBucketValue (Public):  
                returns the current value of the results in bucket.
                
            args:    bucket:int - the id of the counter to be updated
            return:  _eventTotalAry:int - the current value of the bucket.
        '''

        return self._eventTotalAry[bucket]
    # end of getBucketValue
    
    def getPathList(self):        
        '''
            getPathList (Public):  
                returns the path of the current ball.
                
            args:    none
            return:  _evtList:int - the list containing the results of each event at the pegs.
        '''
        #print (self._evtList)
        return str(self._evtList)
    # end of getPathList
    
    def getResultsArray(self):
        '''
            getResultsArray (Public):  
                returns the current value of the results in bucket.
                
            args:    bucket:int - the id of the counter to be updated
            return:  _eventTotalAry:int - the current value of the bucket.
        '''
        print (f'In getResultsArray: {self._eventTotalAry}')
        return self._eventTotalAry
        
    def getResultsInLists(self):
        
        #for key in range(self._eventTotalAry):
        #print (f'{key}, {self._eventTotalAry[key]}')
        print (f'{self._eventTotalAry}')
        return

# end of class GaltonBoardResultTracking