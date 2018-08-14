

def func_validateArgs(self):
    self.debug()

    self.debug('source = ' + self.args.source)

    if self.args.source == 'all':
        self.action = 'check-all'
        self.source = 'all'
    ## source = github
    elif (self.args.source == 'github') or (self.args.source == 'mozilla'):
        self.source = self.args.source
        if (self.args.source == 'github') and (not self.args.user == False):
            self.action = 'user'
        elif (not self.args.add == False):
            self.action = 'add'
        elif (not self.args.remove == False):
            self.action = 'remove'
        else:
            self.action = 'check'

    self.debug('action = ' + self.action)
    return self.action