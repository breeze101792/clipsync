import sys
from core.configtools import *
from cliphal.clipbase import *
from cliphal.terminal import *
from cliphal.macclip import *
from cliphal.pyclip import *
from cliphal.pyclipboard import *
from cliphal.testclip import *
from cliphal.asrclip import *
from utility.debug import *

class ClipManager:
    def __init__(self):

        dbg_info('Clip mode:', Config._args.clip_mode)

        dbg_debug('MacClip(mac)       : ' , MacClip.isSupported())
        dbg_debug('PyClip(win)        : ' , PyClip.isSupported())
        dbg_debug('PyClipboard(linux) : ' , PyClipboard.isSupported())
        dbg_debug('Terminal           : ' , Terminal.isSupported())
        dbg_debug('ASRClip            : ' , ASRClip.isSupported())

        if MacClip.getModeString() == Config._args.clip_mode:
            self._clip_hal = MacClip()
        elif PyClip.getModeString() == Config._args.clip_mode:
            self._clip_hal = PyClip()
        elif PyClipboard.getModeString() == Config._args.clip_mode:
            self._clip_hal = PyClipboard()
        elif Terminal.getModeString() == Config._args.clip_mode:
            self._clip_hal = Terminal()
        elif TestClip.getModeString() == Config._args.clip_mode:
            self._clip_hal = TestClip()
        elif ASRClip.getModeString() == Config._args.clip_mode:
            self._clip_hal = ASRClip(device_index = int(Config._args.device_index))

        elif MacClip.isSupported():
            self._clip_hal = MacClip()
        elif PyClip.isSupported():
            self._clip_hal = PyClip()
        elif PyClipboard.isSupported():
            self._clip_hal = PyClipboard()
        elif Terminal.isSupported():
            dbg_warning('Using Termianl Clips will not work on GUI System')
            self._clip_hal = Terminal()
        else:
            dbg_warning('Using Termianl Clips will not work on GUI System, please check help message for more info')
            self._clip_hal = ClipBase()

        dbg_info('Using Clip Hal: ', type(self._clip_hal))

    def getClipInstance(self):
        return self._clip_hal
