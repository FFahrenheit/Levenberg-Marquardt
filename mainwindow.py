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
        
        self.ui.begin_button.clicked.connect(self.start_algorithm)
        self.ui.clear_button.clicked.connect(self.clear_all)

        self.draw_chart()
        self.initilize_algorithm()

    @Slot()
    def clear_all(self):
        if self.is_running:
            return        

    @Slot()
    def start_algorithm(self):
        if self.is_running:
            return        
 
    def initilize_algorithm(self):
        self.is_running = False
        self.data = []

    def handle_onclick(self, event):
        if event.inaxes is None or self.is_running:
            return
        
        x, y = event.xdata, event.ydata
        
        if event.button == LEFT_CLICK:
            result = 1
            self.ax.plot(x, y, 'bo')
        elif event.button == RIGHT_CLICK:
            result = -1
            self.ax.plot(x, y, 'ro')
        else:
            return

        self.canvas.draw()
        self.data.append([x, y, result])

    def draw_chart(self):
        self.ax = self.figure.add_subplot(111)

        self.ax.set_xlabel('x1')
        self.ax.set_ylabel('x2')
        self.ax.xaxis.set_label_coords(0.95, 0.5)
        self.ax.yaxis.set_label_coords(0.5, 0.95)

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        self.ax.axhline(0, color='black', linewidth=0.8)
        self.ax.axvline(0, color='black', linewidth=0.8)

        self.cid = self.figure.canvas.mpl_connect('button_press_event', self.handle_onclick)
        self.colorbar = None
