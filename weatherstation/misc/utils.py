"""utils for setting locale and getting well formated time"""

import os
import platform
import locale
import time


def read_api_key(path):
    """read api key from given path"""
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise ValueError("no key found at given path: " + path)
    with open(path) as f:
        return f.readline().strip()


def set_locale_de():
    """set the current locale to German or de_DE.utf8 (depending on the os)"""
    try:
        if platform.system() == "Windows":
            locale.setlocale(locale.LC_ALL, "German")
        else:
            locale.setlocale(locale.LC_ALL, "de_DE.utf8")
    except locale.Error:
        pass


def get_time_human_readable():
    """
    returns well formated time string.
    for example: Donnerstag, 21:00
    """
    return time.strftime("%A, %H:%M")
