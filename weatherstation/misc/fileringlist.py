"""FileRingList scans a directory for all files and creates a ring list from these files"""

import os
import glob


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
