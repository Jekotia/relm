##
## relm.storage.list

def func_list(self):
    '''
    Handoff function for listing storage entries. Executes the list method for the configured storage type.
    Arguments:
    self
    '''
    self.debug()

    run = 'self.storage.' + self.config['STORAGE']['type'] + '.list(self)'
    myList = eval(run)
    self.debug()
    return myList