# GaltonBoard
## Purpose
The purpose of this project is to simulate a Galton Board for the purposes of demonstrating
how binomial statistics work.  I love creating games and programs that demonstrate aspects
of mathematics for others to learn.
## References
There is a Jupyter Notebook in the JupyterNotebook folder that describes the project in more
technical detail.  It also includes the derivations of the mean and variance for the Binomial
Distribution as well as how the Poisson and Guassian Distributions are derived from the 
Binomial Distribution.
## Getting Stared with the Galton Board simulator.
### Main Menu Options
#### Board
The Board menu option allows the user to start, stop, pause and resume a simulation.
#### Statistics
The Statistics menu option creates a pop out window showing the accumulated number of balls in each bucket in real time.  It is updated every 5 seconds.
#### Help
The Help menu option displays the About screen with details pertaining to the state of the program code.
### How Start Simulation:
To start a simulation the user will navigate to the Board menu and select Start.
The user will be required to input: 
the depth of the board (default = 7)
the number of balls to traverse the board (default = 100)
the interval timer between starting a ball (default = 100 ms).  A timer value of 0 will cause the simulator to go as fast as possible.
### Viewing Results:
The user can view the path taken by the ball at the top of the main screen.  At the bottom of the main screen, there are 2 rows of output. 
The top row is the accumulated number of balls in a bucket.
The bottom row (green) is the expected number of balls for each bucket.
The expectation value is based on the number of balls defined by the user, the depth of the board and the index of the bucket.
