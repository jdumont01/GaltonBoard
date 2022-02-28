# MplCanvas.py

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,                          # Gets passed into MplCanvas
    NavigationToolbar2QT as NavigationToolbar   # Toolbar for graphics window
)
import      matplotlib
from        matplotlib.figure import Figure
matplotlib.use('Qt5Agg')    # Used to integrate matplotlib with PyQt5

# Module version
__version__ = '0.1'
__author__ = 'Joe Dumont'
__releaseDate__ = '2021-Dec-20'

class MplCanvas(FigureCanvasQTAgg):
    """General use class to display matplotlib objects"""
    """Ref https://www.pythonguis.com/tutorials/plotting-matplotlib/ """
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
