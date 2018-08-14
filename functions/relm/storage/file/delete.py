
## relm.storage.file.delete
import os

def func_delete(self):
    self.debug()

    loop = 0
    dirPath = self.config['STORAGE']['file_path']
    length = len(self.current['path']) - 1
    while loop < length:
        dirPath = os.path.join(dirPath, self.current['path'][loop])
        loop = loop + 1
    filePath = os.path.join(dirPath, self.current['path'][length] + '.json')

    software = self.current['software']


    if os.path.exists(filePath):
        try:
            os.remove(filePath)
        except:
            self.log('warn', 'Failed to remove ' + software + ' from storage for \'' + self.source + '\'')
        else:
            self.log('event', 'Removed \'' + software + '\' from storage for \'' + self.source + '\'')

            startDir = os.path.join(self.config['STORAGE']['file_path'])
            dir = os.path.dirname(filePath)
            while not dir == startDir:
                rmdir(self, dir)
                dir = os.path.dirname(dir)
    else:
           self.info('No such item to remove: ' + filePath)
           return False

def rmdir(self, dirPath):
    if len(os.listdir(dirPath)) == 0:
        try:
            os.rmdir(dirPath)
        except:
            self.log('warn', 'Failed to remove empty directory: ' + dirPath)
            return True
        else:
            self.log('event', 'Removed empty directory: ' + dirPath)
            return True
    else:
        return True
