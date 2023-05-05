from cliphal.clipbase import *
from datetime import datetime

class TestClip(ClipBase):
    def __init__(self):
        self._clip_buffer = ''
        self._g_cnt = 1
        self._interval = 20
        self._current_buffer = ''
    def setBuffer(self, byte_buffer):
        return byte_buffer
    def _interval_send(self):
        self._current_buffer = 'getBuffer'
    def _large_data_send(self):
        self._interval = 10
        self._current_buffer = '''
        '''
    def getBuffer(self):
        if self._g_cnt > 100000000:
            self._g_cnt = 1
        elif self._g_cnt % self._interval == 0:
            # self._interval_send()
            self._large_data_send()

            self._current_buffer += datetime.now().__str__()
        self._g_cnt += 1
        return self._current_buffer


