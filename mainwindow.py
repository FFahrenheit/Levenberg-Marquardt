from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog
from PySide6.QtCore import Slot, QTimer
from ui_mainwindow import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import gc

LEFT_CLICK = 1
RIGHT_CLICK = 3

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ui.plot_area.addWidget(self.canvas)
        