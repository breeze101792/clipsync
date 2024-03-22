import traceback
from cliphal.clipbase import *
from utility.debug import *

try:
    # this two package is require for pyclip
    import win32clipboard
    import win32con
except Exception as e:
    # dbg_error(e)
    # traceback_output = traceback.format_exc()
    # dbg_error(traceback_output)
    pass

try:
    import pyclip
except Exception as e:
    pass

class PyClip(ClipBase):
    def __init__(self):
        pass
    def _setBuffer(self, byte_buffer):
        try:
            return pyclip.copy(byte_buffer)
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
    def _getBuffer(self):
        try:
            return pyclip.paste()
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
        return None

    @staticmethod
    def isSupported():
        try:
            return pyclip.paste()
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
            return False
        return True

    @staticmethod
    def getModeString():
        return 'pyclip'
