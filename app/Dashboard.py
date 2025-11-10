from PyQt5.QtWidgets import *
from Core import *
from DashboardWidgets import *


class Dashboard(MainDashboard):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # DEFINE WIDGETS
        # Define all widgets in correct order! The order of dashboard widgets sets the memory layout for the internal data
        # storage which is then used for data transmission.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.button1 = PushButton("Button 1")
        self.button2 = PushButton("Button 2")
        self.button3 = PushButton("Button 3")
        self.vectorPlot = VectorPlot()
        self.rudderPlot = RudderPlot()
        self.numericDisplayInt32 = NumericDisplayInt32()
        self.numericDisplayFloat32 = NumericDisplayFloat32(num_digits=2)


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # LAYOUT
        # Set the layout for all widgets in the dashboard.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 1, 0)
        layout.addWidget(self.button3, 2, 0)
        layout.addWidget(self.vectorPlot, 0, 1)
        layout.addWidget(self.rudderPlot, 1, 1)
        layout.addWidget(self.numericDisplayInt32, 2, 1)
        layout.addWidget(self.numericDisplayFloat32, 3, 1)
