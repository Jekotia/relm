
## relm.storage.file.write
import json, os

def func_write(self, data):
    self.debug()

    loop = 0
    dirPath = self.config['STORAGE']['file_path']
    length = len(self.current['path']) - 1
    while loop < length:
        dirPath = os.path.join(dirPath, self.current['path'][loop])
        loop = loop + 1
    filePath = os.path.join(dirPath, self.current['path'][length] + '.json')

    if not os.path.exists(dirPath):
        self.debug(dirPath + ' does not exist. Will attempt to create')
        try:
            os.makedirs(dirPath)
        except:
            self.log('error', dirPath + ' does not exist and could not be created')
            return False
    else:
        self.debug(dirPath + ' exists')

    self.debug(filePath)
    try:
        file = open(filePath,'w')
        file.write(json.dumps(data))
        file.close()
    except:
        self.log('error', 'failed to write file ' + filePath)
        pass
        return False
    else:
        return True
