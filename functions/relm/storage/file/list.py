##
## relm.storage.file.list
import os, sys

def func_list(self):
    self.debug()
    self.debug(self.current)
    source = self.current['source']

    if (not self.current['user'] == False):
        path = os.path.join(self.config['STORAGE']['file_path'], source + '_user', self.current['user'])
    else:
        path = os.path.join(self.config['STORAGE']['file_path'], source)

    self.debug('path = ' + path)

    #sys.exit()

    if (os.path.exists(path)):
#        elif (source == 'github'):
        for fname in os.listdir(path):
            if fname.endswith('.json'):
    #        elif source == 'mozilla':
                myList = { source: [] }
                self.debug('loop ' + source)
                for software in os.listdir(path):
                    software = software.split('.')
                    software = software[0]
                    self.debug('loop -- ' + software)
                    #self.checkOne(source, source, software)
                    myList[source].append(software)
            else:
                myList = {}
                for developer in os.listdir(path):
                    myList[developer] = []
                    self.debug('loop ' + developer)
                    target = os.listdir(os.path.join(path, developer))
                    for software in target:
                        software = software.split('.')
                        software = software[0]
                        myList[developer].append(software)
                        self.debug('loop -- ' + software)
                        #self.actions.checkOne(self)
            break
        return myList
    else:
        self.log('warn', 'Storage of type "file" for source ' + source + ' does not exist')
        self.debug(path)
        return False