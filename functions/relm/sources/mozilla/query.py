
## relm.sources.mozilla.query
import json

def func_query(self):
    self.debug()

    software = self.current['software']
    url = 'https://product-details.mozilla.org/1.0/' + software.lower() + '_versions.json'
    self.debug('API URL: ' + url)

    query = self.sources.get(self, url)
    self.debug()
    jsonQuery = json.loads(query.text)
    return jsonQuery
