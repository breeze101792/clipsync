#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# system function
import sys
import traceback
from optparse import OptionParser
import time

from core.core import *
from network.server import *
from utility.debug import *
from core.configtools import *

def main():
    parser = OptionParser(usage='Usage: clipsync [options] ......')
    parser.add_option("-t", "--test", dest="test",
                    help="testing function", action="store_true")
    parser.add_option("-d", "--debug", dest="debug",
                    help="debug mode on!!", action="store_true", default=False)
    parser.add_option("-i", "--server-ip", dest="server_ip", default=None,
                    help="Specify server ip address", action="store")
    parser.add_option("-p", "--server-port", dest="server_port", default=None, type='int',
                    help="Specify server port", action="store")
    parser.add_option("-s", "--start-server", dest="server", default=False,
                    help="Start server", action="store_true")
    parser.add_option("-m", "--clip-mode", dest="clip_mode",
                      help="Choose clip mode(HAL), Mode: pyclip/clipboard/macclip/terminal", action="store")
    parser.add_option("-c", "--config-path", dest="config",
                    help="Start server", action="store")
    # parser.add_option("-l", "--list", dest="list",
    #                 help="List words on wordbank", action="store_true")
    # parser.add_option("-L", "--word-level", dest="word_level",
    #                 help="Setup Word Level", action="store")
    #parser.add_option("-L", "--word-level", dest="word_level",
    #                help="Setup Word Level", default=[], action="append")

    (options, args) = parser.parse_args()
    # Config
    ################################################################
    cfg_mgr = ConfigManager(Config)
    if options.config is not None:
        cfg_mgr.load(options.config)
    else:
        cfg_mgr.load()

    if options.debug is True:
        Config.log_level = 'Debug'
    else:
        Config.log_level = 'Information'

    if options.server_ip is not None:
        Config.Server.ip = options.server_ip
    if options.server_port is not None:
        Config.Server.port = options.server_port

    if options.clip_mode is not None:
        Config._args.clip_mode = options.clip_mode

    # Presetting
    ################################################################
    if DebugSetting.setDbgLevel(Config.log_level) is False:
        Config.log_level = 'Information'
        dbg_warning('Debug level setting fail. rollback to {}'.format(Config.log_level))
        DebugSetting.setDbgLevel(Config.log_level)
    dbg_debug('Server Info:{}:{}'.format(Config.Server.ip, Config.Server.port))

    # Main code start
    ################################################################
    thread_ins = None
    try:
        if options.server is True:
            dbg_info("Starting clipsync server")
            thread_ins = Server()
        else:
            dbg_info("Starting clipsync")
            thread_ins = Core()

        thread_ins.setServerInfo(server_ip=Config.Server.ip, server_port=Config.Server.port)
        thread_ins.start()

    except (KeyboardInterrupt):
        dbg_info("clipsync: exit")
    except Exception as e:
        dbg_error(e)

        traceback_output = traceback.format_exc()
        dbg_error(traceback_output)
    finally:
        if thread_ins is not None:
            thread_ins.quit()
        sys.exit()

if __name__ == '__main__':
    main()
