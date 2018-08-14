
## relm.sources.mozilla.path

def func_path(self):
    self.debug()

    source = self.current['source']
    software = self.current['software']
    return [ source, software ]
