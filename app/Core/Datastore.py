import threading


# Global storage for application state with thread-safe access.
class Datastore:
    def __init__(self):
        self.__input_lock = threading.Lock()
        self.__input_data_size = 0
        self.__input_data = bytearray(self.__input_data_size)
        self.__output_data_size = 0
        self.__output_data = bytearray(self.__output_data_size)
        self.widgets = []

    # add a new widget and allocate IO memory
    def addWidget(self, widget):
        self.widgets.append(widget)

        # required memory size for input and output data
        data_size = widget.requiredIODatastoreSize()
        input_size = data_size[0]
        output_size = data_size[1]

        # add widget to input data
        widget.offsetInputData = self.__input_data_size
        self.__input_data.extend(bytearray(input_size))
        self.__input_data_size += input_size

        # add widget to output data
        widget.offsetOutputData = self.__output_data_size
        self.__output_data.extend(bytearray(output_size))
        self.__output_data_size += output_size

    # write bytes to input data at given offset
    def write_input(self, offset, data_bytes):
        with self.__input_lock:
            if offset < 0 or offset >= self.__input_data_size:
                return
            end = min(offset + len(data_bytes), self.__input_data_size)
            self.__input_data[offset:end] = data_bytes[:end - offset]

    # read bytes from input data at given offset
    def read_input(self, offset, length):
        with self.__input_lock:
            if offset < 0 or offset >= self.__input_data_size:
                return bytes()
            end = min(offset + length, self.__input_data_size)
            return bytes(self.__input_data[offset:end])

    # write bytes to output data at given offset
    def write_output(self, offset, data_bytes):
        if offset < 0 or offset >= self.__output_data_size:
            return
        end = min(offset + len(data_bytes), self.__output_data_size)
        self.__output_data[offset:end] = data_bytes[:end - offset]

    # get the entire output data as bytes
    def get_output(self):
        return bytes(self.__output_data)

    # write memory layout of all widgets to json file
    def write_layout_to_file(self, filename):
        import json
        layout = []
        for widget in self.widgets:
            data_size = widget.requiredIODatastoreSize()
            input_size = data_size[0]
            output_size = data_size[1]
            layout.append({
                'class': widget.__class__.__name__,
                'input_offset': widget.offsetInputData,
                'input_size': input_size,
                'output_offset': widget.offsetOutputData,
                'output_size': output_size
            })
        with open(filename, 'w') as f:
            json.dump(layout, f, indent=4)

# global datastore instance
datastore = Datastore()
