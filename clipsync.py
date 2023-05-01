#!/usr/bin/env python3
# system function
import sys
import traceback
from optparse import OptionParser
# import os
# import subprocess as sp
# import time

from utility.cli import CommandLineInterface as cli
from utility.debug import *
from core.core import *
from utility.debug import *



def main():
    parser = OptionParser(usage='Usage: clipsync [options] ......')
    parser.add_option("-t", "--test", dest="test",
                    help="testing function", action="store_true")
    parser.add_option("-d", "--debug", dest="debug",
                    help="debug mode on!!", action="store_true")
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
        # DebugSetting.setDbgLevel('Disable')

    # open file
    core = Core()
    try:
        dbg_info("debug Terminal")
        core.start()

    except (KeyboardInterrupt):
        dbg_info("DTerm: exit")
    except Exception as e:
        dbg_error(e)

        traceback_output = traceback.format_exc()
        dbg_error(traceback_output)
    finally:
        core.quit()
        sys.exit()


if __name__ == '__main__':
    main()
