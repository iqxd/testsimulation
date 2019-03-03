
import device_oprs

CONFIG_FILE_PATH = './config.txt'


def get_device_type(name: str)->str:
    with open(CONFIG_FILE_PATH, 'r') as file:
        for line in file:
            try:
                cfg_name, cfg_dtype, cfg_connstr = (
                    x.strip() for x in line.split('#'))
            except ValueError:
                pass
            else:
                if cfg_name == name:
                    return cfg_dtype, cfg_connstr
        else:
            raise BaseException(
                'cannot find enough information for device %s in config' % name)


class Device:

    def __init__(self, name: str):
        self.name = name

        self._dtype, self._connstr = get_device_type(name)
        self._open = getattr(device_oprs, self._dtype+'_open')
        self._close = getattr(device_oprs, self._dtype+'_close')
        self._setget = getattr(device_oprs, self._dtype+'_setget')
        self.allmodes = getattr(device_oprs, self._dtype+'_allmodes')
