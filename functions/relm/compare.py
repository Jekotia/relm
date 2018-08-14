
## relm.compare

def func_compare(self, storageData, apiData, json):
    self.debug()
    
    updated = False
    sVer = storageData.split(".")
    aVer = apiData.split(".")

    y = 0
    while y < len(aVer):
        self.debug('aVer[' + str(y) + ']: ' + aVer[y])
        self.debug('sVer[' + str(y) + ']: ' + sVer[y])
        if int(aVer[y]) > int(sVer[y]):
            self.debug('NEW RELEASE')
            self.log('event', 'New release found for ' + self.current['software'])
            updated = True
            break
        y = y + 1

    if updated:
        json['status'] = "updated"
    else:
        json['status'] = "not-updated"
    return json