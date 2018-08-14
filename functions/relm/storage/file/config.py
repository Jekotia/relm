##
## relm.storage.file.config
import configparser

def func_config(self, config):
    config['STORAGE'] = {
        "type": "file",
        "file_path": "./releases"
    }

    return config