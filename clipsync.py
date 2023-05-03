#!/usr/bin/env python3
# system function
import sys
import traceback
from optparse import OptionParser
import time
# import os
# import subprocess as sp
# import time

from core.core import *
from network.server import *
from utility.debug import *



def main():
    parser = OptionParser(usage='Usage: clipsync [options] ......')
    parser.add_option("-t", "--test", dest="test",
                    help="testing function", action="store_true")
    parser.add_option("-d", "--debug", dest="debug",
                    help="debug mode on!!", action="store_true", default=True)
    parser.add_option("-i", "--server-ip", dest="server_ip", default='127.0.0.1',
                    help="Specify server ip address", action="store")
    parser.add_option("-p", "--server-port", dest="server_port", default=65432,
                    help="Specify server port", action="store")
    parser.add_option("-s", "--start-server", dest="server", default=False,
                    help="Start server", action="store_true")
    # parser.add_option("-l", "--list", dest="list",
    #                 help="List words on wordbank", action="store_true")
    # parser.add_option("-L", "--word-level", dest="word_level",
    #                 help="Setup Word Level", action="store")
    #parser.add_option("-L", "--word-level", dest="word_level",
    #                help="Setup Word Level", default=[], action="append")

    (options, args) = parser.parse_args()
    if options.debug is True:
        # DebugSetting.debug_level = DebugLevel.MAX
        DebugSetting.setDbgLevel('Debug')
        dbg_info('Enable debug Mode')
    else:
        DebugSetting.setDbgLevel('Error')
        DebugSetting.setDbgLevel('information')
        # DebugSetting.setDbgLevel('Disable')

    if options.server is True:
        try:
            srv = Server()
            srv.setServerInfo(server_ip=options.server_ip, server_port=options.server_port)
            srv.start()

        except (KeyboardInterrupt):
            dbg_info("clipsync: exit")
        except Exception as e:
            dbg_error(e)

            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
        finally:
            srv.quit()
            sys.exit()
    else:
        core = Core()
        core.setServerInfo(server_ip=options.server_ip, server_port=options.server_port)
        try:
            dbg_info("clipsync")
            core.start()

        except (KeyboardInterrupt):
            dbg_info("clipsync: exit")
        except Exception as e:
            dbg_error(e)

            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
        finally:
            core.quit()
            sys.exit()


if __name__ == '__main__':
    main()
