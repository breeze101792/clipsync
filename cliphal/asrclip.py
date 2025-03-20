import traceback
from cliphal.clipbase import *
from utility.debug import *

try:
    from cliphal.hal.halasr import *
except Exception as e:
    dbg_error(e)
    traceback_output = traceback.format_exc()
    dbg_error(traceback_output)
    pass

class ASRClip(ClipBase):
    def __init__(self, device_index = 0):
        self.asr = ASRService(device_index = device_index)
        # disable punctuation
        self.asr.start()
    def _setBuffer(self, byte_buffer):
        # we don't support this.
        pass
    def _getBuffer(self):
        try:
            clip_buf = self.asr.get()
            if clip_buf is not None:
                dbg_trace(clip_buf)
                return clip_buf.encode('utf8')
            else:
                return None
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
        return None

    @staticmethod
    def isSupported():
        # try:
        #     return pyclip.paste()
        # except Exception as e:
        #     dbg_error(e)
        #     traceback_output = traceback.format_exc()
        #     dbg_error(traceback_output)
        #     return False
        return True

    @staticmethod
    def getModeString():
        return 'asrclip'
