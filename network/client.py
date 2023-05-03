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
        self.host = "127.0.0.1"  # The server's hostname or IP address
        self.port = 65431  # The port used by the server

        self.socket = None
        self.service_threading = None
        self._package_handler = self._def_pkg_hadler
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
        self.socket.connect((self.host, self.port))
        # self.socket.sendall(b"Hello, world")
        while self.flag_run:
            try:
                data = self.socket.recv(1024)
                pkg = Package.fromBytes(data)

                self._package_handler(pkg.content)
                time.sleep(self.interval)
            except Exception as e:
                dbg_error(e)

                traceback_output = traceback.format_exc()
                dbg_error(traceback_output)
                time.sleep(self.interval)

        # close connectiong
        dbg_info('End of Service ')
        self.socket.close()
        self.quit()

if __name__ == "__main__":

    DebugSetting.setDbgLevel('Debug')
    client = Client()
    client.start()
    client.send('Hello Word')
    time.sleep(3)
