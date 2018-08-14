##
## relm.sources.github.config
import configparser

def func_config(self, config):
    config["GITHUB"] = {
        "token": ""
    }
    return config