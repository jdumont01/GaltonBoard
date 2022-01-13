import math
import matplotlib.pyplot as plt
import numpy as np

SMALL_BOARD_DEPTH = 10

def binomialCoefficient(n: int, k: int):
    """Ensure n and k and the return value are integers"""
    nFactorial = math.factorial(n)
    kFactorial = math.factorial(k)
    diffFactorial = math.factorial(n - k)
    
    return int(nFactorial/(kFactorial * diffFactorial))

def probabilityForBucket(c: int, t: int):
    """Calculate the probability of reaching each endpoint."""
    return float(c/t)

def addLabelValues(buckets, values):
    """Add the y value to a bar."""
    for i in range(len(buckets)):
        plt.text(i,values[i],values[i], ha = 'center',
                 bbox = dict(facecolor = 'red', alpha =0.8))    
    
    return    
 
def plotResults(dataDict):
    """Plot a bar graph of the results"""
    buckets = list(dataDict.keys())
    values = list(dataDict.values())
    nBuckets = len(buckets)
    
    fig = plt.figure(figsize = (15, 5))    
    plt.bar(buckets, values, color = 'blue', width = 0.5)
    
    plt.xlabel("Bucket Number")
    plt.xticks(buckets)
    plt.ylabel("Number of Paths to Bucket\n(aka Binomial Coefficient)")
    plt.title(f'Histogram of Expected Paths For Board Depth {nBuckets:d}')
    
    # The plot looks messy if the y-values are printed for large boards.
    if len(buckets) <= SMALL_BOARD_DEPTH:
        addLabelValues(buckets, values)
    plt.show()
    
    return

def printHeader(boardDepth : int , totalPaths : int ):
    """boardDepth (int), totalPaths (int)
        Print a common header for tabular output.
    """        
    print (f'**** Galton Board Output for Depth {boardDepth} ****')
    if boardDepth <= SMALL_BOARD_DEPTH:
        print (f'**** Possible Paths {totalPaths:d} ')
    else:
        print (f'**** Possible Paths {totalPaths:2.6e} ')

    return

def printData( boardDepth : int , totalPaths : int, bucket : int, coeff : int, prob : float ):
    """boardDepth (int), totalPaths (int), bucket (int), coeff (int), prob (float)
        prints the data in csv format
    """       
    # special formatting based on the expected size of the numbers
    if boardDepth <= SMALL_BOARD_DEPTH:
        print (f'{bucket:6d},{coeff:15d},{coeff:10d}/{totalPaths:d},{prob:4.6f}')
    else:
        print (f'{bucket:6d},{coeff:2.5e},{coeff :2.5e}/{totalPaths:2.5e},{prob:2.5e}')
    
    return
    
def generateData(boardDepth : int , totalPaths : int ):
    """boardDepth (int), totalPaths (int)
        return a list of data
    """
    data = []
    
    print (f'Bucket, Possible Paths, Probability Frac, Probability')
    for bucket in range(boardDepth + 1):
        b = binomialCoefficient(boardDepth, bucket)
        p = probabilityForBucket(b, totalPaths)
       
        printData(boardDepth, totalPaths, bucket, b, p)
        
        # add to the list of data    
        data.append(b)
 
    return data
    
def createPlot(data):
    """data is a list.
       This method will convert the list to a dictionary and pass it
       to a function to create a plot.
    """
    dataDict = {}

    # the dictionary needs to be zero based as the index is the bucket number
    for i in range(len(data)):
        dataDict[i]= data[i]
        
    plotResults(dataDict)

    return
    
    
# Client side code
def main(boardDepth = 7):
    totalPaths = 2 ** boardDepth
    
    printHeader(boardDepth, totalPaths)
    data = generateData(boardDepth, totalPaths)
    createPlot(data)
    
    return
    
# main method
if __name__ == '__main__':
    main()