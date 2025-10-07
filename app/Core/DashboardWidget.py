from PyQt5.QtWidgets import QSizePolicy
from abc import abstractmethod
from Core import *
from Core.Datastore import datastore


class DashboardWidget:
    def __init__(self):
        self.offsetInputData = 0
        self.offsetOutputData = 0
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        datastore.addWidget(self)

    # get memory size for input and output data
    @abstractmethod
    def requiredIODatastoreSize(self):
        pass

    # serialize output data to bytes
    @abstractmethod
    def packOutput(self):
        pass

    # deserialize input data from bytes
    @abstractmethod
    def unpackInput(self, data):
        pass

    # update the widget from the datastore
    def updateFromDatastore(self):
        data_size = self.requiredIODatastoreSize()
        input_size = data_size[0]
        output_size = data_size[1]
        input_data = datastore.read_input(self.offsetInputData, input_size)
        self.unpackInput(input_data)
        output_data = self.packOutput()
        if len(output_data) == output_size:
            datastore.write_output(self.offsetOutputData, output_data)
        self.update()
