import sys
from cliphal.clipbase import *
from cliphal.terminal import *
from cliphal.macclip import *
from cliphal.pyclip import *
from utility.debug import *

class ClipManager:
    def __init__(self):
        # self._clip_hal = Base()

        # if sys.platform == 'darwin' and False:
        # if sys.platform == 'darwin':
        if MacClip.isSupported():
            self._clip_hal = MacClip()

        elif PyClip.isSupported():
            self._clip_hal = PyClip()
        elif Terminal.isSupported():
            self._clip_hal = Terminal()
        else:
            self._clip_hal = ClipBase()

        dbg_info('Using Clip Hal: ', type(self._clip_hal))

    def getClipInstance(self):
        return self._clip_hal
