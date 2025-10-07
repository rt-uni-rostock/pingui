# pingui Application
This directory contains the python-based dashboard GUI application.
To run the application you need to have python3 with PyQt5 installed.

#### Installation (Linux)
Install python3 and required modules with the following command.

```
sudo apt install python3 python3-pyqt5
```

#### Installation (Windows)
Download and install python3 from python.org.
Run the following command to install required modules.

```
pip3 install pyqt5
```

## Launch Application
To launch the application run:

```
python3 main.py
```

When launching the application, a `memoryLayout.json` file is created.
This file represents the memory layout for the application's internal data storage, e.g. which widget data is located at which offset.


## UDP Message Protocol
The application periodically sends messages with a rate of about 60 Hz.
This message contains the binary data of all widgets.
An overview of all widgets and their output data size is written to the `memoryLayout.json` file.
Each widget has an `output_offset` and `output_size` value indicating the zero-based offset and the number of bytes that correspond to the binary data of that widget.
The actual interpretation of bytes depends on the widget.
When sending binary data to **pingui**, send an offset address (uint32) followed by a variable number of bytes to write starting from the offset address.

#### Network Settings
  - **Byte-order**: machine, e.g. little-endian
  - **Multicast Group**: 239.192.168.11
  - **Local Port**: 11077
  - **Destination Port**: 11088
  - **Transmission Period**: 16 ms (approx. 60 Hz)

#### Message to **pingui**
A message send to **pingui** must have the following format.

| Offset | Datatype  | Name          | Description                                                                                                |
|:------ |:--------- |:------------- |:---------------------------------------------------------------------------------------------------------- |
| 0      | uint32    | offsetAddress | Offset address from where to start writing binary data to the internal data storage of **pingui**.         |
| 4      | N x uint8 | data          | Bytes to be written to the internal data storage of **pingui** starting from the specified offset address. |

The actual interpretation of the data bytes depend on the type of widget and is shown below.

#### Message from **pingui**
The application sends one UDP message containing the binary output data of all dashboard widgets.
Thus a message would be `bytes_widget_1` `bytes_widget_2` `...` `bytes_widget_N`.
The actual format depends on the type and is shown below.

## Widget Data Specification

### PushButton
**Input** (3 bytes)

| Datatype  | Name  | Description                                        |
|:--------- |:----- |:-------------------------------------------------- |
| 3 x uint8 | color | Color of the button, given as red, green and blue. |

**Output** (1 byte)

| Datatype | Name    | Description                                                  |
|:-------- |:------- |:------------------------------------------------------------ |
| uint8    | counter | Counter that is incremented each time the button is pressed. |

### RudderPlot
**Input** (16 bytes)

| Datatype | Name            | Description                          |
|:-------- |:--------------- |:------------------------------------ |
| float    | commandAngle    | Commanded angle in radians.          |
| float    | commandThrottle | Commanded throttle in range [-1,+1]. |
| float    | actualAngle     | Actual angle in radians.             |
| float    | actualThrottle  | Actual throttle in range [-1,+1].    |

**Output** (0 bytes)

### VectorPlot
**Input** (24 bytes)

| Datatype | Name          | Description                         |
|:-------- |:------------- |:----------------------------------- |
| float    | commandRadius | Commanded radius in range [-1,+1].  |
| float    | commandAngle  | Commanded angle in radians.         |
| float    | commandZ      | Commanded z-value in range [-1,+1]. |
| float    | actualRadius  | Actual radius in range [-1,+1].     |
| float    | actualAngle   | Actual angle in radians.            |
| float    | actualZ       | Actual z-value in range [-1,+1].    |

**Output** (0 bytes)

## Modify the Dashboard
To add or remove GUI elements from the dashboard or rearrange them in a desired layout, open the [Dashboard.py](Dashboard.py) file.
In the constructor, define all dashboard widgets in the correct order.
The order of dashboard widgets sets the memory layout for an internal data storage which is then used for data transmission.
That means, the UDP message protocol depends on the order of widget definition.
After defining all widgets, put them together in a desired layout.

#### Example
In this example, four buttons should be placed in a grid layout.
The final Dashboard.py file would look like this:

```
from PyQt5.QtWidgets import *
from Core import *
from DashboardWidgets import *


class Dashboard(MainDashboard):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # define widgets
        self.button1 = PushButton("Button 1")
        self.button2 = PushButton("Button 2")
        self.button3 = PushButton("Button 3")
        self.button4 = PushButton("Button 4")

        # set layout
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.button1, 0, 0)
        layout.addWidget(self.button2, 1, 0)
        layout.addWidget(self.button3, 0, 1)
        layout.addWidget(self.button4, 1, 1)
```

### Styling
By modifying the [styles.css](styles.css) stylesheet file, some coloring and formatting of the application can be done, e.g. chaning the background color or adjust spacing.

## Implement Custom Widgets
To implement a new custom widget, create a new python class in the [DashboardWidgets](DashboardWidgets/) folder and include this class to the [DashboardWidgets/\_\_init\_\_.py](DashboardWidgets/__init__.py) file.
The class must be derived from the abstract `DashboardWidget` class and a `QWidget`-derived class.
It must implement the following methods:
  - **requiredIODatastoreSize(self)**: return the required size (number of bytes) for input and output data, e.g. `return (1,3)` for 1 byte input and 3 bytes output
  - **packOutput(self)**: return a bytearray that represents the binary output data
  - **unpackInput(self, data)**: unpack input data and adjust the GUI element accordingly

For examples take a look to existing widgets.
