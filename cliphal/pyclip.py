from cliphal.clipbase import *
import traceback
import traceback
try:
    import clipboard
except Exception as e:
    pass

class PyClip(ClipBase):
    def __init__(self):
        pass
    def setBuffer(self, byte_buffer):
        return clipboard.copy(byte_buffer)
    def getBuffer(self):
        return clipboard.paste()
    @staticmethod
    def isSupported():
        try:
            clipboard.paste()
        except Exception as e:
            # print(e)
            # traceback_output = traceback.format_exc()
            # print(traceback_output)
            return False
        return True

