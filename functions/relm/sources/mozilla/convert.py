
## relm.sources.mozilla.convert
import re

def func_convert(self, data):
    self.debug()

    ##print(data)

    source = self.current['source']
    releaseStatus = None
    releaseDeveloper = self.current['developer']
    releaseSoftware = self.current['software']
    releaseVersion = str(data['LATEST_' + releaseSoftware.upper() + '_VERSION'])
    releaseURL = 'https://www.mozilla.org/en-US/' + releaseSoftware + '/' + releaseVersion + '/releasenotes/'
    releaseType = None

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
