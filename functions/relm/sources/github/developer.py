
## relm.sources.github.developer

def func_developer(self, target):
    self.debug()

    output = target.split("/")
    developer = output[0]
    self.debug('developer = ' + developer)
    return developer
