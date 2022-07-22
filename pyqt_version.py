import numpy as np
import pyqtgraph as pg
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from math import sqrt
from random import choice


def midpoint_calculator(point_one, point_two):
    midpoint = (point_one + point_two) / 2
    return midpoint


def random_choice(previous=0):
    if previous == 0:
        point_choice = choice([i for i in range(0, 3)])
        return point_choice
    else:
        point_choice = choice([i for i in range(0, 3) if i not in [previous]])
        return point_choice


class Visualizer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.draw = True
        self.ptr1 = 0
        self.plot_data = None
        self.centralWidget = QWidget()
        self.animate_label = QLabel("Enter Values")
        self.animate_button = QPushButton("Generate!", self)
        self.plot = pg.plot()
        self.layout = QVBoxLayout()
        self.animate_layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.points_top_bottom = QVBoxLayout()
        self.points_button_layout = QHBoxLayout()
        self.size_button_layout = QHBoxLayout()
        self.size_top_bottom = QVBoxLayout()
        self.speed_button_layout = QHBoxLayout()
        self.speed_top_bottom = QVBoxLayout()
        self.points_label = QLabel("Enter Number of Points")
        self.points_box = QLineEdit(self)
        self.points_button = QPushButton('Set Points', self)
        self.size_label = QLabel("Enter Size of Triangle")
        self.size_box = QLineEdit(self)
        self.size_button = QPushButton('Set Size', self)
        self.speed_label = QLabel("Enter Refresh Speed 0-10 (0 = Instantaneous)")
        self.speed_box = QLineEdit(self)
        self.speed_button = QPushButton('Set Speed', self)
        self.first_point = int()
        self.second_point = int()
        self.new_choice = int()
        self.half_height = float()
        self.top_point_x = float()
        self.top_point_y = float()
        self.left_point_x = float()
        self.left_point_y = float()
        self.right_point_x = float()
        self.right_point_y = float()
        self.number_of_points = 10000
        self.all_points_x = []
        self.all_points_y = []
        self.triangle_size = 500
        self.build_array(self.triangle_size, self.number_of_points)
        self.x_array = np.asarray(self.all_points_x)
        self.y_array = np.asarray(self.all_points_y)
        self.refresh_speed = 5
        self.ptr_value = 100
        self.timer_value = 0
        self.count = len(self.x_array)
        self.begin = time.time()
        self.timer_speeds = {1: 50,
                             2: 40,
                             3: 30,
                             4: 20,
                             5: 10,
                             6: 0,
                             7: 0,
                             8: 0,
                             9: 0,
                             10: 0
                             }
        self.ptr_speeds = {1: 1,
                           2: 10,
                           3: 50,
                           4: 80,
                           5: 100,
                           6: 120,
                           7: 140,
                           8: 200,
                           9: 300,
                           10: 400
                           }
        self.setup_ui()

    def update(self):
        self.plot_data.setData(self.x_array[:self.ptr1], self.y_array[:self.ptr1])
        self.ptr1 += self.ptr_value
        if int(((self.ptr1 / self.count) * 100)) % 2 == 0:
            self.report_progress(int(((self.ptr1 / self.count) * 100)))
        if self.ptr1 >= self.count:
            self.report_progress(100)
            self.cleanup()
            self.plot_data.setData(self.x_array, self.y_array)

    def create_triangle(self, side_length):
        self.half_height = (side_length / 2) * (sqrt(3)) / 2
        self.top_point_x = 0
        self.top_point_y = self.half_height
        self.left_point_x = -side_length / 2
        self.left_point_y = -self.half_height
        self.right_point_x = side_length / 2
        self.right_point_y = -self.half_height
        self.all_points_x.extend([self.top_point_x, self.left_point_x, self.right_point_x])
        self.all_points_y.extend([self.top_point_y, self.left_point_y, self.right_point_y])

    def build_array(self, length, dots):
        self.begin = time.time()
        self.create_triangle(length)
        self.first_point = random_choice()
        self.second_point = random_choice(self.first_point)
        self.all_points_x.append(
            midpoint_calculator(self.all_points_x[self.first_point], self.all_points_x[self.second_point]))
        self.all_points_y.append(
            midpoint_calculator(self.all_points_y[self.first_point], self.all_points_y[self.second_point]))
        for _ in range(dots - 4):
            self.new_choice = random_choice()
            self.all_points_x.append(midpoint_calculator(self.all_points_x[self.new_choice], self.all_points_x[-1]))
            self.all_points_y.append(midpoint_calculator(self.all_points_y[self.new_choice], self.all_points_y[-1]))
        self.x_array = np.asarray(self.all_points_x)
        self.y_array = np.asarray(self.all_points_y)
        print(f"Array built in {(time.time() - self.begin):.6f} seconds.")

    def setup_ui(self):
        self.setWindowTitle("Sierpinski Triangle")
        self.resize(1024, 768)
        self.setCentralWidget(self.centralWidget)
        self.animate_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.animate_button.setEnabled(False)
        self.animate_button.clicked.connect(self.animate)
        self.points_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.points_box.setEnabled(False)
        self.points_button.setEnabled(False)
        self.points_button.clicked.connect(self.set_points)
        self.size_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.size_button.clicked.connect(self.set_size)
        self.size_box.setEnabled(False)
        self.size_button.setEnabled(False)
        self.speed_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.speed_box.setEnabled(False)
        self.speed_button.setEnabled(False)
        self.speed_button.clicked.connect(self.set_speed)
        self.layout.addWidget(self.plot)
        self.points_button_layout.addWidget(self.points_box)
        self.points_button_layout.addWidget(self.points_button)
        self.size_button_layout.addWidget(self.size_box)
        self.size_button_layout.addWidget(self.size_button)
        self.speed_button_layout.addWidget(self.speed_box)
        self.speed_button_layout.addWidget(self.speed_button)
        self.points_top_bottom.addWidget(self.points_label)
        self.points_top_bottom.addLayout(self.points_button_layout)
        self.size_top_bottom.addWidget(self.size_label)
        self.size_top_bottom.addLayout(self.size_button_layout)
        self.speed_top_bottom.addWidget(self.speed_label)
        self.speed_top_bottom.addLayout(self.speed_button_layout)
        self.bottom_layout.addLayout(self.points_top_bottom)
        self.bottom_layout.addLayout(self.size_top_bottom)
        self.bottom_layout.addLayout(self.speed_top_bottom)
        self.bottom_layout.addStretch()
        self.animate_layout.addWidget(self.animate_label)
        self.animate_layout.addWidget(self.animate_button)
        self.bottom_layout.addLayout(self.animate_layout)
        self.layout.addLayout(self.bottom_layout)
        self.centralWidget.setLayout(self.layout)
        self.animate()

    def set_points(self):
        textbox_value = self.points_box.text()
        try:
            self.number_of_points = int(textbox_value)
            if self.number_of_points >= 0:
                self.animate_label.setText("Enter Values")
                self.points_button.setEnabled(False)
                self.size_button.setEnabled(True)
                self.points_box.setEnabled(False)
                self.size_box.setEnabled(True)
            else:
                QMessageBox.question(self, 'Message', "Value must be greater than zero.", QMessageBox.Ok,
                                     QMessageBox.Ok)
                self.points_box.setText("")
                self.number_of_points = 500
        except ValueError as err:
            print(err)
            QMessageBox.question(self, 'Message', "\'" + textbox_value + "\' is not a number.  Please enter "
                                                                         "a number.", QMessageBox.Ok, QMessageBox.Ok)
            self.points_box.setText("")

    def set_size(self):
        textbox_value = self.size_box.text()
        try:
            self.triangle_size = int(textbox_value)
            if self.triangle_size >= 0:
                self.size_button.setEnabled(False)
                self.speed_button.setEnabled(True)
                self.size_box.setEnabled(False)
                self.speed_box.setEnabled(True)
                self.build_array(self.triangle_size, self.number_of_points)
            else:
                QMessageBox.question(self, 'Message', "Value must be greater than zero.", QMessageBox.Ok,
                                     QMessageBox.Ok)
                self.size_box.setText("")
                self.triangle_size = 500
        except ValueError as err:
            print(err)
            QMessageBox.question(self, 'Message', "\'" + textbox_value + "\' is not a number.  Please enter "
                                                                         "a number.", QMessageBox.Ok,
                                 QMessageBox.Ok)
            self.size_box.setText("")

    def set_speed(self):
        textbox_value = self.speed_box.text()

        try:
            self.refresh_speed = int(textbox_value)
            if 0 <= self.refresh_speed <= 10:
                self.speed_button.setEnabled(False)
                self.animate_button.setEnabled(True)
                self.animate_label.setText("Ready to Animate!")
                self.speed_box.setEnabled(False)
                if self.refresh_speed != 0:
                    self.set_speed_variables()
            else:
                QMessageBox.question(self, 'Message', "\'" + textbox_value + "\' is not a number between 0 and 10.  "
                                                                             "Please try again.", QMessageBox.Ok,
                                     QMessageBox.Ok)
                self.speed_box.setText("")
        except ValueError as err:
            print(err)
            QMessageBox.question(self, 'Message', "\'" + textbox_value + "\' is not a number.  Please enter "
                                                                         "a number.", QMessageBox.Ok,
                                 QMessageBox.Ok)
            self.speed_box.setText("")

    def set_speed_variables(self):
        self.timer_value = self.timer_speeds[self.refresh_speed]
        self.ptr_value = self.ptr_speeds[self.refresh_speed]

    def start_timer(self):
        self.timer.start(self.timer_value)

    def stop_timer(self):
        self.timer.stop()

    def reset_values(self):
        self.ptr1 = 0
        self.draw = True
        self.points_button.setEnabled(True)
        self.points_box.setEnabled(True)
        self.points_box.setText("")
        self.size_box.setText("")
        self.speed_box.setText("")
        self.all_points_x = []
        self.all_points_y = []

    def cleanup(self):
        self.stop_timer()
        self.reset_values()
        print("Triangle Complete!")
        print(f"Total time elapsed {(time.time() - self.begin):.12f}")
        print(f"Time per point {((time.time() - self.begin) / self.count):.12f}")

    def report_progress(self, n):
        self.animate_label.setText(f"Animation Progress: {n}%")

    def animate(self):
        if self.plot_data is not None:
            self.plot.removeItem(self.plot_data)
            print("Clearing old data")
        self.count = len(self.x_array)
        self.plot_data = self.plot.plot(*[self.x_array, self.y_array], pen=None,
                                        symbolBrush=(0, 213, 255, 255), symbolSize=2)
        self.plot.enableAutoRange()
        self.begin = time.time()
        if self.refresh_speed != 0:
            self.start_timer()
            self.animate_button.setEnabled(False)
        else:
            self.animate_button.setEnabled(False)
            self.cleanup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    program = Visualizer()
    program.show()
    sys.exit(app.exec_())
