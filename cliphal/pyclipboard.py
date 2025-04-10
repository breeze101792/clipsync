import traceback
from cliphal.clipbase import *
from utility.debug import *
try:
    import clipboard
except Exception as e:
    pass

class PyClipboard(ClipBase):
    def __init__(self):
        pass
    def _setBuffer(self, byte_buffer):
        try:
            return clipboard.copy(byte_buffer.decode(encoding='utf8'))
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
        return ''
    def _getBuffer(self):
        try:
            return clipboard.paste().encode('utf8')
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
        return ''
    @staticmethod
    def isSupported():
        try:
            # only try to check if working or not.
            clipboard.paste()
        except Exception as e:
            # dbg_debug(PyClip.getModeString() + ' not supported.')
            # dbg_error(e)
            # traceback_output = traceback.format_exc()
            # dbg_error(traceback_output)
            return False
        return True

    @staticmethod
    def getModeString():
        return 'clipboard'
