import threading
import time
import socket
import traceback
from network.package import *
from network.socketbase import *
from utility.debug import *

class ClientService(SocketBase):
    def __init__(self, connection, address, broadcast):
        super().__init__()
        self.setConnection(connection)
        self.address = address
        self._broadcast = broadcast
        self.regPackageHandler(self.srvBroadcast)

    def srvBroadcast(self, package):
        self._broadcast(package, self.socket.getpeername())
    def start(self):
        self.startService()
    def send(self, package):
        self.sendPackage(package)

class Server(SocketConfig):
    def __init__(self):
        super().__init__()

        self.flag_run = False
        self.socket = None
        self.service_threading = None
        self.client_service = []

    def _wait_connection(self):
        wait_cnt = 100
        while wait_cnt > 0:
            if self.socket is not None:
                return True
            wait_cnt -= 1
            time.sleep(0.1)
        return False

    def quit(self):
        for each_client in self.client_service:
            each_client.quit()

        if self.socket is not None:
            self.socket.close()
        self.flag_run = False
        # self.service_threading.join()
    def start(self):
        self._service()

    def broadcast(self, package, ori_src):
        self._wait_connection()
        # dbg_info('broadcast:',len(self.client_service), ', ',package, )
        dbg_info('broadcast({}):{}'.format(len(self.client_service), package))

        for each_client in self.client_service:
            try:
                if each_client.getPeerHostname()[0] == ori_src[0] and each_client.getPeerHostname()[1] == ori_src[1]:
                    continue
                each_client.send(package)
            except Exception as e:
                dbg_debug(e)

                traceback_output = traceback.format_exc()
                dbg_debug(traceback_output)
                each_client.quit()
                self.client_service.remove(each_client)
    def serverStatus(self):
        dbg_info('Online Connection: {}'.format(len(self.client_service)))
    def startClient(self, client_svc):
        self.client_service.append(client_svc)
        dbg_debug('Start:', self.client_service)
        client_svc.start()
        self.client_service.remove(client_svc)
        dbg_debug('End of client:{}'.format(self.client_service))
        self.serverStatus()

    def _service(self):
        self.flag_run = True

        dbg_info('Start Service on {}:{}'.format(self.server_ip, self.server_port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.modifyBufferSize(self.socket)
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:

        self.socket.bind((self.server_ip, self.server_port))
        self.socket.listen()

        while self.flag_run:
            try:
                # don't need to delay, due to socket timeout
                conn, addr = self.socket.accept()
                dbg_info('connection from : {}'.format(addr))
                client_svc = ClientService(connection = conn, address = addr, broadcast=self.broadcast)

                client_thread = threading.Thread(target=self.startClient, args=(client_svc,))
                client_thread.daemon=True
                client_thread.start()

                time.sleep(self.interval)
            except socket.timeout as e:
                continue
            except Exception as e:
                dbg_error(e)

                traceback_output = traceback.format_exc()
                dbg_error(traceback_output)
                time.sleep(self.interval)

        # close connectiong
        dbg_info('End of Service ')
        self.socket.close()
        self.socket = None

if __name__ == "__main__":
    DebugSetting.setDbgLevel('Debug')
    srv = Server()
    # srv.setServerInfo(server_ip='127.0.0.1', server_port='65432')
    # srv.setServerInfo(server_ip='127.0.0.1')
    srv.setServerInfo(server_ip='10.1.1.17')
    srv.start()
