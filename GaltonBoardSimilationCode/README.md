# Galton Board Simulator
## Purpose
The purpose of this project is to simulate a Galton Board for the purposes of demonstrating
how binomial statistics work.  I love creating games and programs that demonstrate aspects
of mathematics for others to learn.
## References
There is a [Jupyter Notebook](https://github.com/jdumont01/GaltonBoard/blob/main/JupyterNotebook/Galton%20Board.ipynb)
in the JupyterNotebook folder that describes the project in more
technical detail.  It also includes the derivations of the mean and variance for the Binomial
Distribution as well as how the Poisson and Guassian Distributions are derived from the 
Binomial Distribution.

The following website was a great asset to embed matplotlib into PyQT5:
https://www.pythonguis.com/tutorials/plotting-matplotlib/

## Intended Audiences
### Users
Users should be familiar with the basics of combinatorics or just enjoy playing a guessing game of where the ball will land.  
### Development
Python 3.9.1 and PyQT5 were used to develop the simulation.
## Getting Stared with the Galton Board simulator
### Installing the Files
The following files will need to be installed
- BallState.py
- BoardState.py
- GaltonBoard.py
- GaltonBoardBall.py
- GaltonBoardResultTracking.py
- MplCanvas.py
- statisticsView.py
- ./images
- ./images/filled_circle1600.png
- ./images/horizontal-line.png
- ./images/vertical-line.png
### Installing Extra Modules
The following modules will need to be installed (via pip or similar):
- PyQT
- matplotlib
- matplotlib.backends.backend_qt5agg for MplCanvas
### Running the Simulator
Type the following command to start the simulator (assuming the current working directory is the folder where the py files are installed):
python GaltonBoard.py
### Main Menu Options
There are 4 main menu options that are described here.
#### Board
The Board menu option allows the user to start, stop, pause and resume a simulation.
#### Statistics
The Statistics menu option creates a pop out window showing the accumulated number of balls in each bucket in real time.  It is updated every 5 seconds.
#### Help
The Help menu option displays the About screen with details pertaining to the state of the program code.
#### Getting Started
The Getting Started menu options displays the steps needed to start a simulation.
### How Start Simulation
To start a simulation the user will navigate to the Board menu and select Start.
The user will be required to input: 
- the depth of the board (default = 7)
- the number of balls to traverse the board (default = 100)
- the interval timer between starting a ball (default = 100 ms).  A timer value of 0 will cause the simulator to go as fast as possible.
### Viewing Results
The user can view the path taken by the ball at the top of the main screen.  At the bottom of the main screen, there are 2 rows of output. 
The top row is the accumulated number of balls in a bucket.
The bottom row (green) is the expected number of balls for each bucket.
The expectation value is based on the number of balls defined by the user, the depth of the board and the index of the bucket.
