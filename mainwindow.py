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

        self.ui.actionAbrir_dataset.triggered.connect(self.load_dataset)
        self.ui.actionGuardar_dataset.triggered.connect(self.save_dataset)

        self.draw_chart()
        self.initilize_algorithm()

    @Slot()
    def save_dataset(self,):
        if len(self.data) == 0:
            self.print_error("No hay suficientes datos", "Agregue mas patrones de entrenamiento")
            return

        path = QFileDialog.getSaveFileName(
            self,
            'Guardar dataset',
            './datasets',
            'CSV (*.csv)'
        )[0]

        try:
            np.savetxt(path, self.data, delimiter=',', fmt='%f')
        except Exception as e:
            self.print_error("No se pudo guardar el dataset", str(e))

    @Slot()
    def load_dataset(self):
        path = QFileDialog.getOpenFileName(
            self,
            "Abrir dataset",
            "./datasets",
            "CSV Files (*.csv);;All Files (*)"
        )[0]
        
        self.clear_all()
        try:
            with open(path, 'r') as dataset:
                data = dataset.read()
                for line in data.split('\n'):
                    if line.strip() == '':
                        break
                    x, y, result = line.split(',')
                    x = float(x); y = float(y); 
                    result = int(float(result))
                
                    if result == 1:
                        self.ax.plot(x, y, 'bo')
                    elif result == -1:
                        self.ax.plot(x, y, 'ro')

                    self.data.append([x, y, result])
                self.canvas.draw()                    
            
        except Exception as e:
            self.print_error("No se pudo cargar el dataset", str(e))
    
    @Slot()
    def clear_all(self):
        if self.is_running:
            return
        
        plt.clf()
        self.figure.delaxes(self.ax)
        self.draw_chart()
        self.canvas.draw()
        self.ui.iteration_label.setText("-")
        if self.colorbar is not None:
            self.colorbar.remove()
            self.colorbar = None
        self.initilize_algorithm()
        self.ui.result_table.clear()

    @Slot()
    def start_algorithm(self):
        if self.is_running:
            return
        
        if len(self.data) <= 0:
            return self.print_error("Datos insuficientes","No hay suficientes patrones de entrenamiento")
        
        learning_rate = str(self.ui.learning_rate.text())
        max_iterations = str(self.ui.max_iterations.text())
        target_error = str(self.ui.target_error.text())
        mu = str(self.ui.mu.text())
        self.n = self.ui.n_neurons.currentIndex() + 3

        try:
            self.learning_rate = float(learning_rate)
            self.mu = float(mu)
            self.max_iterations = int(max_iterations)
            self.target_error = float(target_error)
        except ValueError:
            return self.print_error("Datos erroneos", "Constante de entrenamiento y error objeto deben ser numericos. Iteraciones maximas debe ser entero")
        
        if self.learning_rate <= 0 or self.learning_rate >= 1:
            return self.print_error("Datos erroneos", "Constante de entrenamiento debe estar entre 0 y 1")
        
        if self.max_iterations < 1:
            return self.print_error("Datos erroneos", " Iteraciones maximas deben ser mayores a 0")
        
        if self.target_error <= 0:
            return self.print_error("Datos erroneos", "Error objetivo debe ser positivo")
        
        if self.mu <= 0 or self.mu > 10:
            return self.print_error("Datos erroneos", "Mu debe estar entre 0.01 y 0.1")
        
        self.init_table()
        self.ui.n_neurons.setEnabled(False)
        self.is_running = True
        self.run_algorithm()

    def run_algorithm(self):
        self.plot_solutions = []
        error = 1e10
        epochs = 0

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

    def print_error(self, title, message):
        QMessageBox.critical(self, title, message)