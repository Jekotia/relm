## relm.sources.github.convert
import re

def func_convert(self, data):
    self.debug()

    ##print(data)

    source = self.current['source']
    releaseStatus = None
    releaseDeveloper = self.current['developer']
    releaseSoftware = self.current['software']

    #print(data)
    if 'tag_name' in data:
        releaseType = 'release'
        releaseVersion = re.sub('[-a-zA-Z]', '', str(data['tag_name']))
        releaseURL = str(data['html_url'])
    elif 'name' in data:
        releaseType = 'tag'
        releaseVersion = re.sub('[-a-zA-Z]', '', str(data['name']))
        releaseURL = 'https://github.com/' + releaseDeveloper + '/' + releaseSoftware + '/releases/tag/' + str(data['name'])

    releaseDict = { 'source': source,
                    'status': releaseStatus,
                    'developer': releaseDeveloper,
                    'software': releaseSoftware,
                    'version': releaseVersion,
                    'url': releaseURL,
                    'type': releaseType
                    }
    self.debug(releaseDict)
    return releaseDict
