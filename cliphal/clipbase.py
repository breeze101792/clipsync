
class ClipBase:
    def __init__(self):
        self.clip_buffer = ''
    def setBuffer(self, data):
        self.clip_buffer = data
    def getBuffer(self):
        return self.clip_buffer
    @staticmethod
    def isSupported():
        return True

