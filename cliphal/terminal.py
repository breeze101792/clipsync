from cliphal.clipbase import *
from utility.debug import *

class Terminal(ClipBase):
    def __init__(self):
        self.clip_buffer = ''
    @staticmethod
    def getModeString():
        return 'terminal'
