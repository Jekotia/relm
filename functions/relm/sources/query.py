
## relm.sources.query

def func_query(self):
    self.debug()

    source = self.current['source']
    self.debug('source = ' + source)
    run = 'self.sources.' + source + '.query(self)'
    query = eval(run)
    self.debug()
    return query
