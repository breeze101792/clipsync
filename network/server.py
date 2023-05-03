import threading
import time
import socket
import traceback
from network.package import *
from utility.debug import *

class ClientService:
    def __init__(self, connection, address, broadcast):
        self.connection = connection
        self.address = address
        self.broadcast = broadcast
        self.interval = 0.1
        self.timeout = 0.1

        self.flag_run = False
        self.connection.settimeout(self.timeout)
    def start(self):
        self._service()
    def quit(self):
        self.flag_run = False
        # self.service_thread.join()
    def send(self, package):
        if package is not None:
            dbg_debug('[{}]: send "{}"'.format(self.address, package))
            self.connection.sendall(package)
    def _service(self):
        self.flag_run = True

        while self.flag_run:
            try:
                data = self.connection.recv(4096)
                if len(data) != 0:
                    dbg_debug('[{}]: "{}"'.format(self.address, data))
                    self.broadcast(data)
                else:
                    time.sleep(self.interval)
            except socket.timeout as e:
                continue
            except BrokenPipeError as e:
                dbg_debug('[{}]'.format(self.address), e)
            except Exception as e:
                dbg_error('[{}]'.format(self.address), e)

                traceback_output = traceback.format_exc()
                dbg_error('[{}]'.format(self.address), traceback_output)
                time.sleep(self.interval)

        dbg_info('[{}]: Connection End.'.format(self.address))
        self.connection.close()

class Server:
    def __init__(self):
        self.flag_run = False
        self.interval = 0.1
        self.timeout = 0.1
        self.server_ip = '127.0.0.1'
        self.server_port = 65432

        self.socket = None
        # self.service_threading = None
        self.client_service = []

    def setServerInfo(self, server_ip = '127.0.0.1', server_port=65432):
        self.server_ip = server_ip
        self.server_port = server_port
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
        self.flag_run = False
        # self.service_threading.join()
    def start(self):
        # self.service_threading = threading.Thread(target=self._service)
        # self.service_threading.daemon=True
        # self.service_threading.start()
        self._service()

    def broadcast(self, package):
        self._wait_connection()
        dbg_debug('broadcast:', package, len(self.client_service))
        for each_client in self.client_service:

            try:
                each_client.send(package)
            except Exception as e:
                dbg_debug(e)

                traceback_output = traceback.format_exc()
                dbg_debug(traceback_output)
    def startClient(self, client_svc):
        self.client_service.append(client_svc)
        dbg_debug('Start:', self.client_service)
        client_svc.start()
        self.client_service.remove(client_svc)
        dbg_debug('After:', self.client_service)
        # client_ins = 
        # del self.client_svc[client_svc]
    def _service(self):
        self.flag_run = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:

        self.socket.bind((self.server_ip, self.server_port))
        self.socket.listen()
        dbg_info('Start Service ')

        while self.flag_run:
            try:
                # don't need to delay, due to socket timeout
                conn, addr = self.socket.accept()
                dbg_info('connect to : {}'.format(addr))
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

if __name__ == "__main__":
    DebugSetting.setDbgLevel('Debug')
    srv = Server()
    # srv.setServerInfo(server_ip='127.0.0.1', server_port='65432')
    # srv.setServerInfo(server_ip='127.0.0.1')
    srv.setServerInfo(server_ip='10.1.1.17')
    srv.start()
