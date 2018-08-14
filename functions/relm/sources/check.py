#
## relm.sources.check
import sys

def func_check(self):

    ##
    ## TESTING VAR
    ##
    ##self.args.source = 'github_user'

    self.debug()
    self.debug(self.current)

    source = self.args.source

    if source == 'all':
        ## for each source in storage, run that sources' check
        for x in self.sourcesList:
            self.current['source'] = x
            run = 'self.sources.' + x + '.check(self)'
            self.debug('Calling ' + run)
            eval(run)
            self.debug()
        '''
        self.sources.github.check(self)
        self.debug()
        self.sources.mozilla.check(self)
        self.debug()
        '''
        return

    else:
        if (not self.args.user == False):
            self.current['source'] = source + '_user'
        else:
            self.current['source'] = source

        self.debug('Checking for ' + self.current['source'])
        run = 'self.sources.' + self.current['source'] + '.check(self)'
        check = eval(run)
        self.debug()
        return check
