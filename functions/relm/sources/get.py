
## relm.sources.get
import requests

def func_get(self, url, headers={}):
    self.debug()

    result = requests.get(url, headers=headers)
    self.debug()
    return result
