## relm.sources.github.check
import json, os, sys

def func_check(self):
    self.debug()

    self.current['source'] = 'github'
    source = self.current['source']
    
    self.debug('source = ' + source)

    self.debug('Checking for new releases in storage for GitHub')

    checkList = self.storage.list(self)
    self.debug(checkList)
    #sys.exit()
    
    if (not checkList == False):
        for owner in checkList:
            self.debug('owner = ' + owner)
            for repo in checkList[owner]:
                self.debug('repo = ' + repo)

                ## ##
                self.current['developer'] = owner
                self.current['software'] = repo

                self.current['path'] = self.sources.path(self)

                ## Make an API query
                query = self.sources.query(self)
                self.debug()

                ## Convert the API query data into the value pairs we use
                apiResult = self.sources.convert(self, query)
                self.debug()

                ## Load the previously stored data
                storageResult = self.storage.read(self)
                self.debug()

                ## Check if the software in question is in storage
                if (not storageResult == False):
                    latest = self.compare(storageResult['version'], apiResult['version'], apiResult)
                    self.debug()
                    if latest['status'] == "updated":
                        if self.notification.send(self, latest, storageResult):
                            self.debug()
                            self.storage.write(self, latest)
                            self.debug()
                            #return True
                        #else:
                            #return False
                    else:
                        self.info(self.current['software'] + ' has not been updated.')
                        #return False
                    ##self.debug(json.dumps(latest))
                #else:
                #    pass
                #    self.storageWrite(source, developer, software, apiResult, user)
                else:
                    self.debug(self.current['software'] + ' was not found in storage')
                    #return False
        return True
    else:
        self.log('warn', 'Storage for GitHub is empty.')
        return False
    self.common.oops()
