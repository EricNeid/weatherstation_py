# WeatherStation

This is a small application using python kivy and openweathermap to display the current weather and forecast.

## Dependencies

It uses pipenv for managing the dependencies and requires python3. Please have a look at the Pipfile.

## Installing

The requirements can be installed using the provided makefile.

If you are using linux, you can set the name of your python exectuable and pip executable in the makefile (for example PYTHON=python3).

You should also set the python version in Pipfile. Get your version by using **python3 --version**.

## using raspberry touch display

If you are using the official Raspberry Pi touch display, you need to configure Kivy to use it as an input source. To do this, edit the file ~/.kivy/config.ini and go to the [input] section. Add this:

mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
