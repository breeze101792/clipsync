import threading
import time
import socket
import traceback
from network.package import *
from network.socketbase import *
from utility.debug import *

class Client(SocketBase):
    def __init__(self):
        super().__init__()
    def start(self):
        self.startThread()
    def send(self, content):
        self.sendData(content)
    def connectionLostHandler(self):

        retry_cnt = 0
        # while retry_cnt < 1000:
        while True:
            time.sleep(1)
            try:
                dbg_info('Try Reconnect({}) {}:{}'.format(retry_cnt, self.server_ip, self.server_port))
                self.socket.connect((self.server_ip, self.server_port))
            except Exception as e:
                dbg_debug('Reconnect fail:{}:{}'.format(self.server_ip, self.server_port))
                # return False
                # print(e)

                # traceback_output = traceback.format_exc()
                # print(traceback_output)
            retry_cnt += 1
        return True

if __name__ == "__main__":

    DebugSetting.setDbgLevel('Debug')
    client = Client()
    client.setServerInfo(server_ip='10.1.1.17')
    client.start()
    client.send('Hello Word')
    time.sleep(3)
