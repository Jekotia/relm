
## relm.sources.github_user.path
import sys

def func_path(self):
    self.debug()

    source = 'github_user'
    user = self.current['user']
    developer = self.current['developer']
    software = self.current['software']
    output = [ source, user, developer, software ]
    return output

'''
user = self.current['user']
source = self.current['source']
developer = self.current['developer']
software = self.current['software']
return [ user, source, developer, software ]
'''