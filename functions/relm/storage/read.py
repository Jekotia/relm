
## relm.storage.read

def func_read(self):
    self.debug()

    run = 'self.storage.' + self.config['STORAGE']['type'] + '.read(self)' #run = 'self.storage.r.' + self.config['STORAGE']['type'] + '(self)'
    output = eval(run)
    self.debug()
    return output


'''
import json, os
    if self.config['STORAGE']['type'] == 'file':
    source = self.current['source']
    user = self.current['user']
    developer = self.current['developer']
    software = self.current['software']

    if (self.config['STORAGE']['type'] == 'file'):
        if (source == 'github') and (not user == False):
            path = os.path.join(self.config['STORAGE']['file_path'], 'github-user', user, developer, software + '.json')
        elif (source == 'github'):
            path = os.path.join(self.config['STORAGE']['file_path'], source, developer, software + '.json')
        elif (source == 'mozilla'):
            path = os.path.join(self.config['STORAGE']['file_path'], source, software + '.json')

        self.debug('Storage file path: ' + path)
        if (os.path.isfile(path)):
            with open(path, 'r') as fin:
                self.debug('Found in storage')
                return json.loads(fin.read())
        else:
            self.debug('Not found in storage')
            return False
'''
