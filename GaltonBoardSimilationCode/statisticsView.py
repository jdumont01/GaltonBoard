# 
#   File:   statisticsView.py
#   Date:   2-Jan-2022
#   Author: Joe Dumont
#

# Imports 
from        MplCanvas import *
import      numpy as np
from        PyQt5.QtWidgets import (
            #QApplication,           # reason
            QMainWindow,            # create the main UI
            QVBoxLayout,            # create vertical UI with multiple objects
            QWidget,                # used to create a graph widget
            QStatusBar              # status bar
        )

# Module version
__version__ = '0.1'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

class statisticsView(QMainWindow):
    """
        Class:  statisticsView
        This class can display the results array and the expected results
        in a histogram from numpy
               
        Input:      QMainWindow object from the main  UI
        Output:     Creates separate screen displaying the accumulated results of the 
                    simulation.
    """
    def __init__(self, parent=None, refreshPeriod = 100):
        super(statisticsView, self).__init__(parent)
        
        self._refreshPeriod = refreshPeriod
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("border : 2px solid black;")
        self.statusBar.showMessage(f'Starting')
        
        # setting title to the window
        self.setWindowTitle('Galton Board Results')

        # setting geometry to the window
        self.setGeometry(100, 100, 800, 800)
        
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self._sc = MplCanvas(self, width=5, height=4, dpi=100)
        self._sc.mpl_connect("motion_notify_event", self._hover)
        
        # default - will be configured later
        self.annot = self._sc.axes.annotate("", xy=(0,0),textcoords="offset points",
                bbox=dict(boxstyle="round", fc="black", ec="b", lw=2),
                arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        
        # toolbar for the graph UI
        self._toolbar = NavigationToolbar(self._sc, self)
        
        # Create layout
        self._graphLayout = QVBoxLayout()
        self._graphLayout.addWidget(self._toolbar)
        self._graphLayout.addWidget(self._sc)
        
        # hold toolbar
        self._graphWidget = QWidget()
        self._graphWidget.setLayout(self._graphLayout)
        self.setCentralWidget(self._graphWidget)
        
        self._initialize()
        
        return
    # end on __init__
            
    def closeWindow(self):
        '''
            closeWindow (Public):  
                Closes the statistics window.
                            
            args:    none
            return:  none
        '''
        self.close()
        
        return
    # end of closeWindow
        
    def _hover(self, event):
        '''
            _hover:  updates the UI with an annotation of the coordinate value associated with the cursor
                    positon
            args:    event:axes object - thrown cursor event  
            return:  none
        '''

        if event.inaxes == self._sc.axes:
            #print(f'event triggered')
            #print(f'{event.xdata}, {event.xdata}, {self._sc.axes}, {self._plot}')
            #if event in self._plot:
            #print(f'in update')
            #cont, ind = self._plot.contains(event)
            #if cont:
            self._update_annot(event)
            self.annot.set_visible(True)
            self._sc.draw_idle()
        else:
            self.annot.set_visible(False)                
            
        #if vis:
        #    self.annot.set_visible(False)
        #    self._sc.draw_idle()        
        
        return
    # end of _hover

    def _update_annot(self, event):
        '''
            _update_annot:  update the annotation string
            args:    event:object - thrown cusor event
            return:  none
        '''
        print(f'in _update_annot')
        x = event.xdata
        y = event.ydata
        self.annot.xy = (x,y)
        text = "({:d},{:d})".format(int(x),int(y))
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

        return
    # end of _update_annot
        
    def _initialize(self):
        '''
            _initialize:  
            args:    none
            return:  none
        '''
        
        return
    # end of _initialize

    def update(self):
        '''
            update (Public):  Updates the statistics UI
            args:    none
            return:  none
        '''
        self.refreshTimer.stop()
        self.refreshResultsHistogram()
        
        return
    # update
        
    def timerEvent(self, event):
        '''
            timerEvent (Public):  test function to notify the user when the timer was triggered.
            args:    none
            return:  none
        '''
        if event.timerId() == self.refreshTimer.timerId():
            print (f'Refresh Timer triggered')
            self.statusBar.showMessage(f'Timer Event {event} ')
        
        return
    # timerEvent
        
    def _getPlotText(self):
        '''
            _getPlotText:  Set the statistics UI title and axes labels  
            args:    none
            return:  none
        '''
        self._sc.axes.set_title('Results from Galton Board')
        self._sc.axes.set_xlabel('Bucket Number')
        self._sc.axes.set_ylabel('Frequency')

        return
    # _getPlotText
        
    def refreshResultsHistogram(self, data):
        '''
            refreshResultsHistogram (Public):  refresh the UI  
            args:    data:list - list of data to plot
            return:  none
        '''
        #print (f'refreshResultsHistogram {data}')
        bins = []
        hist = []
        binsOut = []
        
        #self._sc.axes.clear()
        #self._sc.axes.set_frame_on(True)
        #self._sc.axes.set_axis_on()
        #self._sc.axes.grid(True)
        self._sc.axes.cla()
        self._getPlotText()
        
        for i in range(len(data)):
            bins.append(i)
            
        hist, binsOut = np.histogram(data, bins=bins)
        #print (f'data = {data}')
        #print (f'hist = {hist}')
        #print (f'bins = {binsOut}')
        
        self._plot = self._sc.axes.plot(bins, data, '-', color='blue')
        #self.setCentralWidget(self._sc)        
        self.annot = self._sc.axes.annotate("", xy=(0,0),textcoords="offset points",
                xytext=(50, 50), bbox=dict(boxstyle="round", fc="black", ec="b", lw=2),
                arrowprops=dict(arrowstyle="->"))

        self._sc.draw()
    
        return
    # end fo refreshResultsHistogram
        
    def displayResultsHistogram(self, data):
        '''
            displayResultsHistogram (Public):  Displays the statistics UI  
            args:    data:list - list of data to plot
            return:  none
        '''
        bins = []

        self._getPlotText()
        
        for i in range(len(data)):
            bins.append(i)
            
        hist, binsOut = np.histogram(data, bins=bins)
        #print (f'data = {data}')
        #print (f'hist = {hist}')
        #print (f'bins = {binsOut}')
        
        self._plot = self._sc.axes.plot(bins, data, '-', color='blue')
        
        #self.setCentralWidget(self._sc)
        
        self._sc.show()
   
        return
    # end of displayResultsHistogram