import kivy.app
import platform

from weatherstation import utils, gui_weatherstation

LOCATION = "Erkner,de"
API_KEY_FILE = "./weatherstation/assets/api.key"

def run():
    utils.set_locale_de()

    kivy.core.window.Window.size = (800, 480)
    if platform.system() != "Windows":
        kivy.core.window.Window.fullscreen = True

    gui_weatherstation.WeatherStationApp(LOCATION, utils.read_api_key(API_KEY_FILE)).run()
