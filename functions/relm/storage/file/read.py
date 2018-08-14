## relm.storage.file.read
import json, os, sys

def func_read(self):
    self.debug()

    #print(__qualname__)
    #import inspect
    #frm = inspect.stack()[1]
    #mod = inspect.getmodule(frm[0])
    #print('[%s] %s' % (mod.__name__))
    #print(inspect.stack()[1])

    #print(self.current['path']);sys.exit()

    #print(self.current['path'])
    #print('hi') ; sys.exit()
    dirPath = self.config['STORAGE']['file_path']
    loop = 0
    length = len(self.current['path']) - 1
    while loop < length:
        dirPath = os.path.join(dirPath, self.current['path'][loop])
        loop = loop + 1
    filePath = os.path.join(dirPath, self.current['path'][length] + '.json')

    self.debug('Storage file path: ' + filePath)
    if (os.path.isfile(filePath)):
        with open(filePath, 'r') as fin:
            self.debug('Found in storage')
            output = json.loads(fin.read())
            return output
    else:
        self.debug('Not found in storage')
        return False
