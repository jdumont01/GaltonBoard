# Filename: hello.py

"""Simple Hello World example with PyQt5."""

import sys

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import (QApplication,
    QLabel, 
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QWidget)

# 2. Create an instance of QApplication
app = QApplication(sys.argv)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        layout = QGridLayout()
        widget=layout.addWidget()
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

    return

# *****
# Python entry point
# *****
if __name__ == "__main__":
    main()
    
    sys.exit(app.exec_())

    print ("Done!")    
