
## relm.storage.delete

def func_delete(self):
    self.debug()

    run = 'self.storage.' + self.config['STORAGE']['type'] + '.delete(self)' #run = 'self.storage.d.' + self.config['STORAGE']['type'] + '(self)'
    output = eval(run)
    self.debug()
    return output