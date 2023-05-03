import threading
import time
import socket
import traceback
from network.package import *
from utility.debug import *

class Client:
    def __init__(self):
        self.flag_run = False
        self.interval = 0.1
        # hard code for testing
        self.server_ip = '127.0.0.1'
        self.server_port = 65432

        self.socket = None
        self.service_threading = None
        self._package_handler = self._def_pkg_hadler
    def setServerInfo(self, server_ip = '127.0.0.1', server_port=65432):
        self.server_ip = server_ip
        self.server_port = server_port
    def _def_pkg_hadler(self, content):
        dbg_print('Content:', content.__str__())

    def regPackageHandler(self, handler):
        self._package_handler = handler
    def _wait_connection(self):
        wait_cnt = 100
        while wait_cnt > 0:
            if self.socket is not None:
                return True
            wait_cnt -= 1
            time.sleep(self.interval)
        return False

    def quit(self):
        self.flag_run = False
        self.service_threading.join()
    def send(self, content):
        self._wait_connection()
        tmp_pkg = Package()
        # tmp_pkg.type    = ''
        # tmp_pkg.srcip   = ''
        # tmp_pkg.destip  = ''
        # tmp_pkg.length  = ''
        tmp_pkg.content = content
        self.socket.sendall(tmp_pkg.toBytes())
    def start(self):
        self.service_threading = threading.Thread(target=self._service)
        self.service_threading.daemon=True
        self.service_threading.start()

    def _service(self):
        self.flag_run = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))
        # self.socket.sendall(b"Hello, world")
        while self.flag_run:
            try:
                data = self.socket.recv(1024)
                if len(data) != 0:
                    pkg = Package.fromBytes(data)
                    self._package_handler(pkg.content)

            except Exception as e:
                dbg_error(e)

                traceback_output = traceback.format_exc()
                dbg_error(traceback_output)
            finally:
                time.sleep(self.interval)

        # close connectiong
        dbg_info('End of Service ')
        self.socket.close()

if __name__ == "__main__":

    DebugSetting.setDbgLevel('Debug')
    client = Client()
    client.setServerInfo(server_ip='10.1.1.17')
    client.start()
    client.send('Hello Word')
    time.sleep(3)
