
## relm.sources.github.query
import json

def func_query(self):
    self.debug()

    #source = 'github'
    developer = self.current['developer']
    software = self.current['software']
    if self.config['GITHUB']['token'] == '':
        headers = { }
    else:
        headers = { 'Authorization': 'token ' + self.config['GITHUB']['token'] }

    loop = 0
    while loop <= 2:
        if loop == 0:
            kind = 'releases'
        elif loop == 1:
            self.info('Could not find releases for ' + developer + '/' + software + 'on github. Will try tags')
            kind  = 'tags'
        elif loop == 2:
            self.log('error', 'Could not find releases or tags for ' + developer + '/' + software + ' on GitHub')
            return False

        url='https://api.github.com/repos/' + developer + '/' + software + '/' + kind
        self.debug('API URL: ' + url)

        query = self.sources.get(self, url, headers)
        self.debug()
        jsonQuery = json.loads(query.text)
        self.debug()
        if json.dumps(jsonQuery) == '[]':
            self.debug('Empty response. Likely no ' + kind + ' for target')
        else:
            break
        
        loop = loop + 1

    for jsonEntry in jsonQuery:
        break
    return jsonEntry

'''
query = self.query.github('releases', source, developer, software)


    if query == False:
        self.log('error', 'Could not find releases or tags for ' + developer + '/' + software + ' on GitHub')
        return False
    elif not any(char.isdigit() for char in query['name']):
        self.info('Cannot work with non-numerical version in ' + developer + '/' + software)
        return False
    else:
        self.info('Using tags for ' + developer + '/' + software)
        return query
elif not any(char.isdigit() for char in query['tag_name']):
    self.info('Cannot work with non-numerical version in ' + developer + '/' + software)
    return False
else:
    return query
'''
