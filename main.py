# Import

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

# Main Window Object, Settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("PDF Analyzer")
main_window.resize(800, 600)

# Create All Objects in Main Window

# Object Top Centre
title = QLabel("PDF Analyzer")


# Objects Left Column

# Objects right Column

# Design the objects

#Master layout where everything goes into
master_layout = QVBoxLayout()

# Top Centrered Objects in horizontal
title_box = QHBoxLayout()
insert_box = QHBoxLayout()

title_box.addWidget(title)

# set up columns that contain objects later
left_column = QVBoxLayout()
right_column = QVBoxLayout()

# rows in left column
left_row1 = QHBoxLayout()
left_row2 = QHBoxLayout()
left_row3 = QHBoxLayout()

# rows in right column
right_row1 = QHBoxLayout()
right_row2 = QHBoxLayout()

# add to Layout
master_layout.addLayout(title_box, Qt.AlignmentFlag.AlignHCenter)
master_layout.addLayout(insert_box)

left_column.addLayout(left_row1)
left_column.addLayout(left_row2)
left_column.addLayout(left_row3)

right_column.addLayout(right_row1)
right_column.addLayout(right_row2)

master_layout.addLayout(left_column, 30)
master_layout.addLayout(right_column, 70)


main_window.setLayout(master_layout)

# Events


# Run the Application
main_window.show()
app.exec()

