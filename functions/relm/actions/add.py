
## relm.actions.add
import sys

def func_add(self): #, source=False, developer=False, software=False, user=False):
    self.debug()

    source = self.current['source']
    developer = self.current['developer']
    software = self.current['software']
    user = self.current['user']

#    if (self.current['source'] == 'github') and (not self.current['user'] == False):
#        msg = self.current['developer'] + '/' + self.current['software']


    ##
    if (self.storage.read(self) == False):
        query = self.sources.query(self)
        if (query == False):
            return False
        else:
            latest = self.sources.convert(self, query)
    elif (source == 'github'):
        if (not user == False):
            self.info(developer + '/' + software + ' is already in storage for source \'github\', user \'' + user + '\'')
            return False
        else:
            self.info(developer + '/' + software + ' is already in storage for source \'github\'')
            return False
    else:
        self.info(software + ' is already in storage for source \'' + source + '\'')
        return

    if self.storage.write(self, latest):
        usrmsg = ''
        if (not user == False):
            usrmsg = ', for user \'' + user + '\''
        self.log('event', 'Added ' + software + ' to storage for source \'' + source + '\'' + usrmsg)
            #self.storageWrite(self.args.source, developer, software, apiResult)
        return True
    self.common.oops()