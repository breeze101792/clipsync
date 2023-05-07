import sys
from cliphal.clipbase import *
from cliphal.terminal import *
from cliphal.macclip import *
from cliphal.pyclip import *
from cliphal.testclip import *
from utility.debug import *

class ClipManager:
    def __init__(self):

        if MacClip.isSupported():
            self._clip_hal = MacClip()

        elif PyClip.isSupported():
            self._clip_hal = PyClip()
        # elif TestClip.isSupported():
        #     dbg_warning('Using Termianl Clips will not work on GUI')
        #     self._clip_hal = TestClip()
        elif Terminal.isSupported():
            dbg_warning('Using Termianl Clips will not work on GUI System')
            self._clip_hal = Terminal()
        else:
            dbg_warning('Using Termianl Clips will not work on GUI System')
            self._clip_hal = ClipBase()

        dbg_info('Using Clip Hal: ', type(self._clip_hal))

    def getClipInstance(self):
        return self._clip_hal
