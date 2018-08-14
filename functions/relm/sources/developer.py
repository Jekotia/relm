
## relm.sources.developer

def func_developer(self, target):
    self.debug()

    source = self.current['source']
    self.debug('source = ' + source)
    run = 'self.sources.' + source + '.developer(self, target)'
    query = eval(run)
    self.debug()
    return query
