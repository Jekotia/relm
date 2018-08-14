
## relm.sources.github.software

def func_software(self, target):
    self.debug()

    output = target.split("/")
    software = output[1]
    self.debug('software = ' + software)
    return software
