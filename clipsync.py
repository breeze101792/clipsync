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

# for audio dev list
from cliphal.asrclip import *

def main():
    parser = OptionParser(usage='Usage: clipsync [options] ......')
    parser.add_option("-a", "--audio-index", dest="device_index",
                        help="Specify the microphone device index.", action="store", default=-1)
    parser.add_option("-l", "--mic-list", dest="mic_list",
                        help="List available microphone devices.", action="store_true", default=False)
    parser.add_option("-t", "--test", dest="test",
                        help="Run testing functions.", action="store_true")
    parser.add_option("-d", "--debug", dest="debug",
                        help="Enable debug mode.", action="store_true", default=False)
    parser.add_option("-i", "--server-ip", dest="server_ip", default=None,
                        help="Specify the server IP address.", action="store")
    parser.add_option("-p", "--server-port", dest="server_port", default=None, type='int',
                        help="Specify the server port.", action="store")
    parser.add_option("-s", "--start-server", dest="server", default=False,
                        help="Start the server.", action="store_true")
    parser.add_option("-m", "--clip-mode", dest="clip_mode",
                        help="Choose the clip mode (HAL, pyclip, clipboard, macclip, terminal, asrclip). Mode: pyclip(windows)/clipboard(linux)/macclip(mac)/terminal/asrclip(audio)", action="store")
    parser.add_option("-c", "--config-path", dest="config",
                        help="Specify the path to the configuration file.", action="store")

    (options, args) = parser.parse_args()
    # Config
    ################################################################
    cfg_mgr = ConfigManager(Config)
    if options.config is not None:
        cfg_mgr.load(options.config)
        cfg_mgr = os.path.expanduser(options.config)
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

    if options.device_index == -1:
        Config._args.device_index = 0
    else:
        Config._args.device_index = options.device_index
        Config._args.clip_mode = 'asrclip'
    if options.mic_list is True:
        ASRClip.listAudioDevice()
        Config._args.device_index = input("Please select your devices index:")
        Config._args.clip_mode = 'asrclip'

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
