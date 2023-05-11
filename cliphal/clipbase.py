import traceback
from utility.debug import *
class ClipBase:
    def __init__(self):
        self.clip_buffer = b''
    def _setBuffer(self, data):
        self.clip_buffer = data
    def _getBuffer(self):
        return self.clip_buffer
    def setBuffer(self, data):
        self._setBuffer(data)
    def getBuffer(self):
        return self._getBuffer()
    @staticmethod
    def isSupported():
        return True
    @staticmethod
    def getModeString():
        return 'dfault'
