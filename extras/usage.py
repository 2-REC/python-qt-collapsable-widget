"""usage.py

    Example usage of the Collapsable Frame widget.
"""

import sys

from Qt.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton
)
from Qt.QtCore import Qt as qt


from collapsable_frame import CollapsableFrame


def run(*args):
    if not QApplication.instance():
        app = QApplication(*args)
    else:
        app = QApplication.instance()

    window = QMainWindow()

    widget = QWidget()
    widget.setMinimumWidth(350)
    window.setCentralWidget(widget)

    layout = QVBoxLayout()
    layout.setAlignment(qt.AlignTop)
    widget.setLayout(layout)


    # Vertical layout widget
    vertical_widget = QWidget()
    vertical_layout = QVBoxLayout()
    vertical_widget.setLayout(vertical_layout)

    vertical_layout.addWidget(QPushButton("Button 1"))
    vertical_layout.addWidget(QPushButton("Button 2"))
    vertical_layout.addWidget(QPushButton("Button 3"))

    # Set widget in collapsable frame
    frame_vertical = CollapsableFrame(title="Vertical")
    frame_vertical.setContent(vertical_widget)
    layout.addWidget(frame_vertical)


    # Grid layout widget
    grid_widget = QWidget()
    grid_layout = QGridLayout()
    grid_widget.setLayout(grid_layout)

    label1 = QLabel("Label 1:")
    label1.setAlignment(qt.AlignVCenter)
    grid_layout.addWidget(label1, 0, 0, 1, 1)
    grid_layout.addWidget(QLineEdit(), 0, 1, 1, 1)

    label2 = QLabel("Label 2:")
    label2.setAlignment(qt.AlignVCenter)
    grid_layout.addWidget(label2, 1, 0, 1, 1)
    grid_layout.addWidget(QLineEdit(), 1, 1, 1, 1)

    # Set widget in collapsable frame
    frame_grid = CollapsableFrame(title="Grid")
    frame_grid.setContent(grid_widget)
    layout.addWidget(frame_grid)

    layout.addStretch(1)

    window.show()
    window.raise_()

    return app.exec_()


if __name__ == "__main__":
    return_code = run(sys.argv)
    sys.exit(return_code)
