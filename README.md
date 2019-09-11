# WeatherStation

This is a small application using python kivy and openweathermap to display the current weather and forecast.

## Dependencies

It uses pipenv for managing the dependencies and requires python3. Please have a look at the Pipfile.

## Installing

The requirements can be installed using the provided makefile or manually.

```bash
pip install --user pipenv
pipenv install --dev
```

## Testing

Tests require that you provide openweathermap api key in assets/api.key for testing.

```bash
pipenv run nosetests
```

## Run application

```bash
pipenv run python weatherstation/gui_weatherstation.py
```

## using raspberry touch display

If you are using the official Raspberry Pi touch display, you need to configure Kivy to use it as an input source. To do this, edit the file ~/.kivy/config.ini and go to the [input] section. Add this:

mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput
