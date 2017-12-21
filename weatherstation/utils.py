"""utils for setting locale and getting well formated time"""

import os
import glob
import platform
import locale
import time


class FileRingList:
    """List of filename, created from given directory"""
    fileNames = []
    i = 0

    def add_directory(self, directory):
        """add files from directory"""
        if not os.path.exists(directory):
            raise ValueError("given directory does not exists: " + directory)
        self.fileNames.extend(glob.glob(os.path.join(directory, '*')))


    def current(self):
        """return current file"""
        if self.i >= len(self.fileNames):
            return ''
        else:
            return self.fileNames[self.i]


    def next(self):
        """return next file"""
        if self.i+1 >= len(self.fileNames):
            self.i = 0
        else:
            self.i += 1
        return self.current()


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
