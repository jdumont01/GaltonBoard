# statisticsView.py

from MplCanvas import *
import      numpy as np
from PyQt5.QtWidgets import (
    QApplication,           # reason
    QMainWindow,            #
    QVBoxLayout,            #
    QWidget,                #
    QStatusBar              #
)

# Module version
__version__ = '0.1'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

class statisticsView(QMainWindow):
    """Display all stats."""
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
        #self.setFixedSize(self._boardWidthPx, self._boardHeightPx)
        
        # This class can display the results array and the expected results
        # in a histogram from numpy
               
        # creating a timer
        #self.refreshTimer = QTimer()
        #self.refreshTimer.timeout.connect(self.update)        
        
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
        
    def __del__(self):
        #del self._sc  
        
        return
    
    def closeWindow(self):
        self.close()
        
        return
        
    def _hover(self, event):
        """Return the value that the mouse is hovering over."""
        # event has motion_notify_event:  xy, xydata, button, dblclick, inaxes
        #vis = self.annot.get_visible()
        #print (f'_hover event = {event}')

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

    def _update_annot(self, event):
        """Print the annotated data."""
        print(f'in _update_annot')
        x = event.xdata
        y = event.ydata
        self.annot.xy = (x,y)
        text = "({:d},{:d})".format(int(x),int(y))
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

        return
        
    def _initialize(self):
        #self.refreshTimer.start(self._refreshPeriod)               
        
        return

    def update(self):
        self.refreshTimer.stop()
        self.refreshResultsHistogram()
        
        return
        
    # time event method
    def timerEvent(self, event):
        # checking timer id
        if event.timerId() == self.refreshTimer.timerId():
            print (f'Refresh Timer triggered')
            self.statusBar.showMessage(f'Timer Event {event} ')
        
        return
        
    def _getPlotText(self):
        self._sc.axes.set_title('Results from Galton Board')
        self._sc.axes.set_xlabel('Bucket Number')
        self._sc.axes.set_ylabel('Frequency')

        return
        
    def refreshResultsHistogram(self, data):
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
        
    def displayResultsHistogram(self, data):
        """displayResultsHistogram"""
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
   