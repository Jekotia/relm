##
## relm.notification.send

def func_send(self, jsonNew, jsonOld):
    self.debug()

    notifyType = self.config['NOTIFICATIONS']['type']

    #self.debug('source = ' + source)
    run = 'self.notification.' + notifyType + '.send(self, jsonNew, jsonOld)'
    notify = eval(run)
    self.debug()
    return notify
