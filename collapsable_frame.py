"""collapsable_frame.py

    A Qt collapsable widget, in the spirit of the Maya 'frameLayout' command.
"""


from Qt.QtCore import (
    QObject,
    Signal,
    QPoint
)
from Qt.QtCore import Qt as qt

from Qt.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)

from Qt.QtGui import (
    QPainter,
    QColor,
    QPalette,
    QPolygon
)


class CollapsableFrame(QWidget):
    def __init__(self, title=None, parent=None):
        super(CollapsableFrame, self).__init__(parent=parent)

        self._is_collasped = False
        self._content = None

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self._title_frame = self.TitleFrame(
            parent=parent,
            title=title,
            collapsed=self._is_collasped
        )
        self.main_layout.addWidget(self._title_frame)

        self.initCollapsable()


    def initCollapsable(self):
        self._title_frame.clicked.connect(self.toggleCollapsed)

    def setCollapsed(self, collapse):
        if collapse != self._is_collasped:
            self.toggleCollapsed()

    def toggleCollapsed(self):
        if self._content:
            self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped
        self._title_frame._arrow.setArrow(int(self._is_collasped))

    def setContent(self, widget):
        if self._content:
            self.main_layout.removeWidget(self._content)

        self._content = widget
        self.main_layout.addWidget(widget, qt.AlignTop)


    class TitleFrame(QFrame):
        clicked = Signal()

        def __init__(self, parent=None, title="", collapsed=False):
            QFrame.__init__(self, parent=parent)

            self.setMinimumHeight(20)
            self.setMaximumHeight(20)
            background_color = self.palette().color(QPalette.Button)
            style = (
                "background: rgb({}, {}, {});"
                "border-radius: 2px;"
            ).format(
                background_color.red(),
                background_color.green(),
                background_color.blue()
            )
            # ~Hack to add borders to the TitleFrame if it has the same color
            #  as the window background
            # ('QPalette.Button' doesn't return the expected button color)
            #TODO(2-REC): fix issue
            if background_color == self.palette().color(QPalette.Window):
                text_color = self.palette().color(QPalette.ButtonText)
                style += (
                    "border: 1px solid rgb({}, {}, {});"
                ).format(
                    text_color.red(),
                    text_color.green(),
                    text_color.blue()
                )
            self.setStyleSheet(style)


            title_layout = QHBoxLayout(self)
            title_layout.setContentsMargins(0, 0, 0, 0)
            title_layout.setSpacing(0)

            self._arrow = self.initArrow(collapsed)

            title_layout.addWidget(self._arrow)
            title_layout.addWidget(self.initTitle(title))

        def initArrow(self, collapsed):
            arrow = CollapsableFrame.Arrow(collapsed=collapsed)
            arrow.setStyleSheet("border: 0px")
            return arrow

        def initTitle(self, title=None):
            title_label = QLabel(title)
            title_label.setMinimumHeight(18)
            title_label.setStyleSheet("border: 0px; font: bold;")
            return title_label

        def mousePressEvent(self, event):
            self.clicked.emit()
            return super(
                CollapsableFrame.TitleFrame,
                self
            ).mousePressEvent(event)


    class Arrow(QFrame):
        def __init__(self, parent=None, collapsed=False):
            QFrame.__init__(self, parent=parent)

            self.setMaximumSize(34, 20)

            # horizontal == 1
            self._arrow_horizontal = QPolygon()
            self._arrow_horizontal.append(QPoint(10, 3))
            self._arrow_horizontal.append(QPoint(15, 8))
            self._arrow_horizontal.append(QPoint(10, 13))

            # vertical == 0
            self._arrow_vertical = QPolygon()
            self._arrow_vertical.append(QPoint(7, 5))
            self._arrow_vertical.append(QPoint(17, 5))
            self._arrow_vertical.append(QPoint(12, 11))

            # arrow
            self._arrow = None
            self.setArrow(int(collapsed))

        def setArrow(self, arrow_dir):
            if arrow_dir:
                self._arrow = self._arrow_horizontal
            else:
                self._arrow = self._arrow_vertical

        def paintEvent(self, event):
            painter = QPainter()
            painter.begin(self)
            color = self.palette().color(QPalette.ButtonText)
            painter.setBrush(color)
            painter.drawPolygon(self._arrow)
            painter.end()
