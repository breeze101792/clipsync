import traceback
from cliphal.clipbase import *
from utility.debug import *

try:
    import clipboard
except Exception as e:
    pass

class PyClip(ClipBase):
    def __init__(self):
        pass
    def setBuffer(self, byte_buffer):
        try:
            return clipboard.copy(byte_buffer)
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
        return ''
    def getBuffer(self):
        try:
            return clipboard.paste()
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
        return ''
    @staticmethod
    def isSupported():
        try:
            clipboard.paste()
        except Exception as e:
            # dbg_error(e)
            # traceback_output = traceback.format_exc()
            # dbg_error(traceback_output)
            return False
        return True

