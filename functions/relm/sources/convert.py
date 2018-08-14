
## relm.sources.convert

def func_convert(self, input):
    self.debug()

    source = self.current['source']
    self.debug('source = ' + source)
    run = 'self.sources.' + source + '.convert(self, input)'
    query = eval(run)
    self.debug()
    return query
