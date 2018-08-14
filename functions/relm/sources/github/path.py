
## relm.sources.github.path

def func_path(self):
    self.debug()

    source = self.current['source']
    developer = self.current['developer']
    software = self.current['software']
    return [ source, developer, software ]