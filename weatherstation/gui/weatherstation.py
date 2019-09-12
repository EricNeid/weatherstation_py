# coding=utf-8
"""gui for weatherstation"""

import os
import datetime
import threading

import kivy.app
import kivy.uix.screenmanager
import kivy.core.window
import kivy.clock
import kivy.logger

from kivy.properties import ObjectProperty, StringProperty
from weatherstation import utils
from weatherstation import model
from weatherstation.api import openweather


INTERVAL_READ_WEATHER_DATA_SEC = 15 * 60
INTERVAL_SCREENSAVER_SEC = 30
INTERVAL_CHECK_CURRENT_SCREEN_SEC = 60 * 60
INTERVAL_UPDATE_CLOCK_SEC = 60

DELAY_OPEN_SCREENSAVER_SEC = 120

# between 6 and 9 the weather gui should be displayed as default
HOURS_SHOW_WEATHER_DEFAULT = range(
    6, # show weather screen after 6 o'clock
    9  # show screensaver after 8 o'clock
)


DIRS_SCREENSAVER = "./weatherstation/resources/screensaver"

BACKGROUND_WEATHER_MAP = {
    "2" : "./resources/assets/background/background_thunder.jpg",
    "3" : "./resources/assets/background/background_drizzle.jpg",
    "5" : "./resources/assets/background/background_rain.jpg",
    "6" : "./resources/assets/background/background_snow.jpg",
    "7" : "./resources/assets/background/background_mist.jpg",
    "8" : "./resources/assets/background/background_clear.jpg",
    "9" : "./resources/assets/background/background_tornado.jpg"
}

def log_i(func):
    """log_i provides a decorator for logging"""
    def log_wrapper(*args, **kwargs):
        """send function call to kivy log"""
        log_entry = "{}()".format(func.__name__)
        kivy.logger.Logger.info(log_entry)
        return func(*args, **kwargs)
    return log_wrapper


def log_exception(error, message):
    """log_exception writes the given exception and optional message to kivy log"""
    log_entry = "{}:\n{}".format(str(error), str(message))
    kivy.logger.Logger.error(log_entry)


class WeatherStationScreenManager(kivy.uix.screenmanager.ScreenManager):
    """handler for screen transitions"""

    def show_weather_screen(self):
        """show weather information and update displayed data async"""
        self.get_weather_screen().update_clock(0) # param is ignored
        self.current = "screen_weather"


    def show_slideshow(self):
        """show screensaver"""
        self.get_slideshow_screen().update_clock(0) # param is ignored
        self.get_slideshow_screen().update()
        self.current = "screen_slideshow"


    def get_weather_screen(self):
        """getter for weather gui"""
        return self.get_screen("screen_weather")


    def get_slideshow_screen(self):
        """getter for weather gui"""
        return self.get_screen("screen_slideshow")


class SlideShow(kivy.uix.screenmanager.Screen):
    """UI for Screensaver"""
    screenmanager = None
    images = utils.FileRingList()

    slide = ObjectProperty(None)
    clock = StringProperty(None)

    def show_weather_gui_screen(self):
        """ask the screenmanager to show weather gui screen"""
        self.screenmanager.transition.direction = "left"
        self.screenmanager.show_weather_screen()
        kivy.clock.Clock.schedule_once(self.show, DELAY_OPEN_SCREENSAVER_SEC)


    def show(self, _):
        """make sure the screenmanager shows the slideshow"""
        self.screenmanager.show_slideshow()


    def add_directory(self, local_dir):
        """add directory to take images from"""
        self.images.add_directory(os.path.abspath(local_dir))


    def update(self):
        """update ui"""
        self.slide.source = self.images.current()


    def next(self, _):
        """display next slide, parameter is required for kivy.clock"""
        self.slide.source = self.images.next()


    def update_clock(self, _):
        """Update displayed time, parameter is required for kivy.clock"""
        self.clock = utils.get_time_human_readable()


class WeatherGui(kivy.uix.screenmanager.Screen):
    """UI to display weather data"""
    app = None
    screenmanager = None
    weather_data = None

    clock = StringProperty(None)

    timestamp = StringProperty(None)
    current_temperature = StringProperty(None)
    today_weather_background = ObjectProperty(None)

    today_daytime_temperature = StringProperty(None)
    today_min_temperature = StringProperty(None)
    today_max_temperature = StringProperty(None)
    today_weather = ObjectProperty(None)

    day_1_daytime_temperature = StringProperty(None)
    day_1_min_temperature = StringProperty(None)
    day_1_max_temperature = StringProperty(None)
    day_1_weather = ObjectProperty(None)

    day_2_daytime_temperature = StringProperty(None)
    day_2_min_temperature = StringProperty(None)
    day_2_max_temperature = StringProperty(None)
    day_2_weather = ObjectProperty(None)


    def show_slide_show_screen(self):
        """ask the screenmanager to show slideshow screen"""
        self.screenmanager.transition.direction = "right"
        self.screenmanager.show_slideshow()


    def update_weather_async(self, _):
        """
        spawn thread to obtain weather data and update ui when finished
        parameter is required for kivy.clock
        """
        threading.Thread(target=self.update_weather).start()


    @log_i
    @kivy.clock.mainthread
    def update_weather(self):
        """download weather data and trigger ui update"""
        try:
            self.weather_data = self.app.get_weather_data()
        except openweather.RetrieveWeatherDataException as error:
            log_exception(error, "could not download data")
            return
        except model.ParseWeatherDataException as error:
            log_exception(error, "downloaded data does not contain expected json")
            return

        if self.weather_data:
            self.timestamp = self.weather_data.timestamp
            self.current_temperature = self.weather_data.current_temperature

            primary_condition_code = self.weather_data.forecast[0].condition_id[0]
            background_ressource = BACKGROUND_WEATHER_MAP[primary_condition_code]
            if background_ressource != self.today_weather_background.source:
                self.today_weather_background.source = background_ressource

            self.today_daytime_temperature = self.weather_data.forecast[0].temperature_day
            self.today_min_temperature = self.weather_data.forecast[0].temperature_min
            self.today_max_temperature = self.weather_data.forecast[0].temperature_max
            self.today_weather.source = openweather.get_url_for_weather(
                self.weather_data.forecast[0].condition_icon)
            self.today_weather.reload()

            self.day_1_daytime_temperature = self.weather_data.forecast[1].temperature_day
            self.day_1_min_temperature = self.weather_data.forecast[1].temperature_min
            self.day_1_max_temperature = self.weather_data.forecast[1].temperature_max
            self.day_1_weather.source = openweather.get_url_for_weather(
                self.weather_data.forecast[1].condition_icon)
            self.day_1_weather.reload()

            self.day_2_daytime_temperature = self.weather_data.forecast[2].temperature_day
            self.day_2_min_temperature = self.weather_data.forecast[2].temperature_min
            self.day_2_max_temperature = self.weather_data.forecast[2].temperature_max
            self.day_2_weather.source = openweather.get_url_for_weather(
                self.weather_data.forecast[2].condition_icon)
            self.day_2_weather.reload()


    def update_clock(self, _):
        """Update displayed time, parameter is required for kivy.clock"""
        self.clock = utils.get_time_human_readable()


class WeatherStationApp(kivy.app.App):
    """app to display current weather and forecast"""
    screenmanager = None

    def __init__(self, city, api_key):
        super().__init__()
        self.city = city
        self.api_key = api_key


    def build(self):
        """
        build app,
        connect screens and schedule updates
        """
        self.load_kv("resources/gui_weatherstation.kv")
        self.screenmanager = self.root

        # init screens
        weather_gui = self.screenmanager.get_weather_screen()
        weather_gui.screenmanager = self.screenmanager
        weather_gui.app = self

        slideshow = self.screenmanager.get_slideshow_screen()
        slideshow.screenmanager = self.screenmanager
        slideshow.add_directory(DIRS_SCREENSAVER)

        # update displayed time
        kivy.clock.Clock.schedule_interval(
            slideshow.update_clock,
            INTERVAL_UPDATE_CLOCK_SEC
        )
        kivy.clock.Clock.schedule_interval(
            weather_gui.update_clock,
            INTERVAL_UPDATE_CLOCK_SEC
        )
        # next screensaver slide
        kivy.clock.Clock.schedule_interval(
            slideshow.next,
            INTERVAL_SCREENSAVER_SEC
        )
        # schedule update of weather data
        kivy.clock.Clock.schedule_interval(
            weather_gui.update_weather_async,
            INTERVAL_READ_WEATHER_DATA_SEC
        )
        # check which screen is to be shown
        kivy.clock.Clock.schedule_interval(
            self.check_current_screen,
            INTERVAL_CHECK_CURRENT_SCREEN_SEC
        )

        # start with screensaver
        self.screenmanager.show_slideshow()
        # update weather data
        weather_gui.update_weather_async(0) # param is ignored

        return self.screenmanager


    def check_current_screen(self, _):
        """check which screen to show"""
        assert self.screenmanager

        hour = datetime.datetime.now().hour
        if hour in HOURS_SHOW_WEATHER_DEFAULT:
            self.screenmanager.show_weather_screen()
        else:
            self.screenmanager.show_slideshow()


    def get_weather_data(self):
        """downloads data for the given location"""
        return openweather.download_weather_data(self.city, self.api_key)
