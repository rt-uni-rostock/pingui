# pingui
A **python**-based GUI application that allows for a fast dashboard development designed for monitoring and control.
Data is transmitted via UDP multicast, with the protocol depending on the content of the dashboard.
By adjusting one python file, the dashboard is modified (e.g. add/remove widgets, layout).
For more information about the application take a look to the [app](app/) directory.

## MATLAB/Simulink
This repository provides a Simulink library to pack and unpack binary data for the **pingui** application.
To use the library, add the [pingui.prj](pingui.prj) project file as reference project to your own MATLAB project tp update the project path.

### Examples
For examples take a look to [examples](examples/).
