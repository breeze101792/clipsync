from cliphal.base import *
from time

class TestClip(base):
    def __init__(self):
        self._clip_buffer = ''
    def setBuffer(self, byte_buffer):
        return byte_buffer
    def getBuffer(self):
        return 'getBuffer'+time.now().__str__()

