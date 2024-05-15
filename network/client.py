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
        connect_status=False

        retry_cnt = 0
        sleep_time = 60
        max_sleep_time = 900

        while connect_status is False:
            time.sleep(sleep_time)

            try:
                dbg_info('[{}] Try Reconnect {}:{}'.format(retry_cnt, self.server_ip, self.server_port))
                self.reConnection()
                connect_status = True
            except Exception as e:
                sleep_time = sleep_time + 60 if sleep_time != max_sleep_time else max_sleep_time
                dbg_debug('-> Reconnect fail:{}:{}, wait for {}'.format(self.server_ip, self.server_port, sleep_time))
                retry_cnt += 1
            #     sleep_time = (sleep_time * 2) % max_sleep_time
            #     dbg_debug('Reconnect fail:{}:{}, wait for {}'.format(self.server_ip, self.server_port, sleep_time))
            #     dbg_debug(e)
            #
            #     traceback_output = traceback.format_exc()
            #     dbg_debug(traceback_output)
            # finally:
                # sleep_time = sleep_time + 60 if sleep_time != max_sleep_time else max_sleep_time
                # dbg_debug('Reconnect fail:{}:{}, wait for {}'.format(self.server_ip, self.server_port, sleep_time))
                # retry_cnt += 1

        dbg_debug('-> Reconnect successfully:{}:{}'.format(self.server_ip, self.server_port))
        return connect_status

if __name__ == "__main__":

    DebugSetting.setDbgLevel('Debug')
    client = Client()
    client.setServerInfo(server_ip='10.1.1.17')
    client.start()
    client.send('Hello Word')
    time.sleep(3)
