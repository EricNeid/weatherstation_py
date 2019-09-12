import kivy.app
import platform

from weatherstation.gui import weatherstation
from weatherstation import utils

LOCATION = "Erkner,de"
API_KEY_FILE = "./weatherstation/resources/api.key"

def run():
    utils.set_locale_de()

    kivy.core.window.Window.size = (800, 480)
    if platform.system() != "Windows":
        kivy.core.window.Window.fullscreen = True

    weatherstation.WeatherStationApp(LOCATION, utils.read_api_key(API_KEY_FILE)).run()
