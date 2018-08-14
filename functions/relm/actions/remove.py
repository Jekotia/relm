
## relm.actions.remove
import os

def func_remove(self):
    self.debug()

    source = self.current['source']
    #developer = self.current['developer']
    software = self.current['software']
    #user = self.current['user']

    if (not self.storage.read(self) == False):
        return self.storage.delete(self)
    else:
        self.info(software + ' is not in storage for source \'' + source + '\'')
        return False
    
    self.common.oops()
    '''
    if (source == 'github'):
        msg = developer + '/' + software
        if (not user == False):
            dirPath = os.path.join(self.config['STORAGE']['file_path'], 'github-user', user, developer)
        else:
            dirPath = os.path.join(self.config['STORAGE']['file_path'], self.source, developer)
        
        filePath = os.path.join(dirPath, software + '.json')
    else:
        dirPath = os.path.join(self.config['STORAGE']['file_path'], self.source)
        filePath = os.path.join(dirPath, software + '.json')
        msg = software
    '''