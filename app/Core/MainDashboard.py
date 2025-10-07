from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from DashboardWidgets import *


class MainDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("dashboard")
