
## relm.sources.software

def func_software(self, target):
    self.debug()

    source = self.current['source']
    self.debug('source = ' + source)
    run = 'self.sources.' + source + '.software(self, target)'
    query = eval(run)
    self.debug()
    return query
