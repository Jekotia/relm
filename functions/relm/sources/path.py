## relm.sources.path
import sys

def func_path(self):
    self.debug()

    source = self.current['source']
    self.debug('source = ' + source)
    if (not self.current['user'] == False):
        run = 'self.sources.' + source + '_user.path(self)'
    else:
        run = 'self.sources.' + source + '.path(self)'
    path = eval(run)
    self.debug()
    return path
