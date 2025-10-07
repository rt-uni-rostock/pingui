from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from Dashboard import Dashboard
from Core import *
from Core.Datastore import datastore


# The main window class is created, when this script is executed, see bottom of the script
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widgetDashboard = Dashboard(self)
        self.setCentralWidget(self.widgetDashboard)
        self.setWindowTitle("Title")
        self.resize(1280, 800)
        # self.setFixedSize(1280,800)
        # self.showFullScreen()

        # save the current memory layout to a json file
        datastore.write_layout_to_file("memoryLayout.json")

        # create and start the network manager thread
        self.networkManager = NetworkManager(group='239.192.168.11', local_port=11077, dest_port=11088)
        self.networkManager.start()

        # 60 Hz timer (approx. 16 ms interval)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onTick)
        self.timer.start(16)

    def onTick(self):
        for widget in datastore.widgets:
            widget.updateFromDatastore()
        self.networkManager.sendOutputData()

    def closeEvent(self, event):
        self.timer.stop()
        self.networkManager.stop()
        super().closeEvent(event)


# If this python script is executed, then the following code is executed.
if __name__ == "__main__":
    # change the executable path to the folder of this script
    import os
    import sys
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # create the application and main window
    app = QApplication([])
    with open("style.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window = MainWindow()
    window.show()
    app.exec()
