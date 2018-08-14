
## relm/storage.write

def func_write(self, data):
    self.debug()

    run = 'self.storage.' + self.config['STORAGE']['type'] + '.write(self, data)' #run = 'self.storage.w.' + self.config['STORAGE']['type'] + '(self, data)'
    output = eval(run)
    self.debug()
    return output

'''
import json, os
def func_write(self, data):
    source = self.current['source']
    user = self.current['user']
    developer = self.current['developer']
    software = self.current['software']
    
    if self.config['STORAGE']['type'] == 'file':
        if (source == 'github') and (not user == False):
            path = os.path.join(self.config['STORAGE']['file_path'], 'github-user', user, developer)
        elif (source == 'github'):
            path = os.path.join(self.config['STORAGE']['file_path'], source, developer)
        elif (source == 'mozilla'):
            path = os.path.join(self.config['STORAGE']['file_path'], source)



        if not os.path.exists(path):
            self.debug(path + ' does not exist. Will attempt to create')
            try:
                os.makedirs(path)
            except:
                self.log('error', path + ' does not exist and could not be created')
                return False
        else:
            self.debug(path + ' exists')

        path = os.path.join(path, software + '.json')

        self.debug(path)
        try:
            file = open(path,'w')
            file.write(json.dumps(data))
            file.close()
        except:
            self.log('error', 'failed to write file ' + path)
            pass
            return False
        else:
            return True
'''