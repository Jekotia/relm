
## relm.sources.mozilla.check
import json, os

def func_check(self):
    self.debug()

    self.current['user'] = False
    self.current['source'] = 'mozilla'
    self.current['developer'] = 'mozilla'

    source = self.current['source']
    
    self.debug('source = ' + source)

    self.debug('Checking for new releases in storage for Mozilla')


    checkList = self.storage.list(self)
    self.debug(checkList)
    if (not checkList == False):
        for developer in checkList:
            for software in checkList[developer]:
                self.debug('software = ' + software)
                self.current['software'] = software
                self.current['path'] = self.sources.path(self)

                ## Make an API query
                query = self.sources.query(self)
                self.debug()

                ## Convert the API query data into the value pairs we use
                apiResult = self.sources.convert(self, query)
                self.debug()
                storageResult = self.storage.read(self)
                self.debug()

                ## Check if the software in question is in storage
                if not storageResult == False:
                    latest = self.compare(storageResult['version'], apiResult['version'], apiResult)
                    self.debug()
                    if latest['status'] == "updated":
                        if self.notification.send(self, latest, storageResult):
                            self.debug()
                            self.storage.write(self, latest)
                            self.debug()
                            return True
                        else:
                            return False
                    else:
                        self.info(self.current['software'] + ' has not been updated.')
                        return False
                else:
                    self.debug(self.current['software'] + ' was not found in storage')
                    return False
    else:
        self.log('warn','Storage for Mozilla is empty.')
        return False
    self.common.oops()
