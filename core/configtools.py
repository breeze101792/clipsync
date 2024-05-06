import sys
import os
import inspect
import json
import traceback
from configparser import ConfigParser
from utility.debug import *

class Config:
    # Read only variable
    version='0.3.0'
    program_name = 'Config Manager'
    config_file = "./config.json"
    log_level = "Information"
    def __init__(self):
        pass
    class _args:
        clip_mode = ''
    class Server:
        ip = "0.0.0.0"
        port = 11320

class ConfigManager:
    def __init__(self, cfg):
        self.cfg = cfg
    def _dump(self, instance, indent=''):
        indent_unit = 2 * ' '
        title_width = 20 - len(indent)

        ins_dict = vars(instance)
        dbg_debug(ins_dict)
        for each_key in ins_dict.keys():
            if each_key.startswith('_') is not True and type(ins_dict[each_key]).__name__  != 'function':
                if inspect.isclass(ins_dict[each_key]):
                    print('{}[{}]'.format(indent, each_key))
                    self._dump(ins_dict[each_key], indent + indent_unit)
                else:
                    print('{}{}: {}'.format(indent, each_key.ljust(title_width), ins_dict[each_key]))
    def dump(self, indent=''):
        self._dump(self.cfg, indent)

    def _dict(self, instance, indent=''):
        indent_unit = 2 * ' '
        title_width = 20 - len(indent)

        ins_dict = vars(instance)
        ret_dict = dict()
        for each_key in ins_dict.keys():
            if each_key.startswith('_') is not True and type(ins_dict[each_key]).__name__  != 'function':
                if inspect.isclass(ins_dict[each_key]):
                    # print('{}[{}]'.format(indent, each_key))
                    ret_dict[each_key] = self._dict(ins_dict[each_key], indent + indent_unit)
                else:
                    # print('{}{}: {}'.format(indent, each_key.ljust(title_width), ins_dict[each_key]))
                    ret_dict[each_key] = ins_dict[each_key]
        return ret_dict
    def toDict(self, indent=''):
        return self._dict(self.cfg, indent)
    def toJson(self):
        tmp_json = json.dumps(self.toDict(), indent=2)
        # dbg_debug(tmp_json.__str__())
        return tmp_json

    def save(self):
        dbg_info('Saving config file: {}'.format(self.cfg.config_file))
        with open(self.cfg.config_file, 'w') as configfile:
            configfile.write(self.toJson().__str__())
    def _loadDict(self, instance, cfg_dict):
        for each_key in cfg_dict.keys():
            if type(cfg_dict[each_key]).__name__ == 'str':
                # self.cfg.__dict__[each_key] = cfg_dict[each_key]
                setattr(instance, each_key, cfg_dict[each_key])
            elif type(cfg_dict[each_key]).__name__ == 'dict':
                # self._loadDict(getattr(instance, each_key) ,cfg_dict[each_key])
                self._loadDict(instance.__dict__[each_key] ,cfg_dict[each_key])
    def loadDict(self, cfg_dict):
        # dbg_print(self.dump())
        for each_key in cfg_dict.keys():
            try:
                if type(cfg_dict[each_key]).__name__ == 'str':
                    continue
                elif type(cfg_dict[each_key]).__name__ == 'dict':
                    # dbg_print(each_key, ', ', getattr(self.cfg, each_key))
                    tmp_ins = self.cfg.__dict__[each_key]

                    self._loadDict(tmp_ins, cfg_dict[each_key])
            except Exception as e:
                dbg_warning(e)

                traceback_output = traceback.format_exc()
                dbg_warning(traceback_output)
    def load(self, config_path=None):
        if config_path is None:
            config_path = self.cfg.config_file

        try:
            with open(config_path, 'r') as configfile:
                dbg_info('load config file from: {}'.format(config_path))
                cfg_buffer = configfile.read()
                tmp_json = json.loads(cfg_buffer)
                self.loadDict(tmp_json)
        except Exception as e:
            dbg_error(e)
            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)


if __name__ == "__main__":
    cfgmgr = ConfigManager()
    # cfgmgr.dump(Config)
    print(cfgmgr.dict(Config))
