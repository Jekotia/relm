
## relm.sources.github_user.check
import json, os, sys

def func_check(self):
    self.debug()
    self.current['user'] = self.args.user
    user = self.current['user']

    self.current['source'] = 'github_user'
    #self.current['path'] = self.sources.path(self)
    #print(self.current['path']) ; sys.exit()

    
    ## Assemble list of starred repos
    self.userStarred = {
        #'b-ryan': ['powerline-shell'],
        'docker': ['docker-ce']
    }
    self.info(self.userStarred)
    '''
    url = 'https://api.github.com/users/' + user + '/starred?per_page=100'
    if self.config['GITHUB']['token'] == '':
        headers = { }
    else:
        headers = { 'Authorization': 'token ' + self.config['GITHUB']['token'] }

    self.debug('API URL: ' + url)
    query = self.sources.get(self, url, headers=headers )
    jsonQuery = json.loads(query.text)

    for jsonEntry in jsonQuery:
        owner = jsonEntry['owner']['login']
        repo = jsonEntry['name']

        if not owner in self.userStarred:
            self.userStarred[owner] = []

        self.userStarred[owner].append(repo)

    self.info(self.userStarred)
    '''
    
    ## Ensure everything in self.userStarred is in storage
    for owner in self.userStarred:
        self.current['developer'] = owner
        self.debug('owner = ' + owner)
        for repo in self.userStarred[owner]:
            self.current['software'] = repo
            self.current['path'] = self.sources.github_user.path(self)
            self.debug('repo = ' + repo)

            if (self.storage.read(self) == False):
                print('do addy type things')
                print('do addy type things')
                self.actions.add(self)
            else:
                print('do updatey type things')
                print('do updatey type things')
                self.sources.github.check(self)
            #query = self.query('github', owner, repo)
    sys.exit()
    ## Assemble list of stored repos
    self.userStored = self.storage.list(self)

    self.info(self.userStored)
    '''
    if (self.config['STORAGE']['type'] == 'file'):
        path = os.path.join(self.config['STORAGE']['file_path'], 'github_user', user)

        if (not os.path.exists(path)):
            self.debug(path + ' does not exist. Will attempt to create')
            try:
                os.makedirs(path)
            except:
                self.log('error', path + ' does not exist and could not be created')
                return False
        else:
            self.debug(path + ' exists')

        for owner in os.listdir(path):
            if not owner in self.userStored:
                self.userStored[owner] = []

            target = os.listdir(os.path.join(path, owner))
            for repo in target:
                repo = repo.split('.')
                repo = repo[0]
                self.userStored[owner].append(repo)
    '''

    ## Compare and remove
    if (not self.userStored == False):
        for owner in self.userStored:
            self.current['developer'] = owner
            if owner in self.userStarred:
                for repo in self.userStored[owner]:
                    self.current['software'] = repo
                    if repo in self.userStarred[owner]:
                        pass
                        self.debug('keep ' + owner + '/' + repo)
                    else:
                        self.debug('del ' + owner + '/' + repo)
                        self.log('event', '\'' + owner + '/' + repo + '\' found in storage for github user \'' + user + '\', but not in the users starred repos. Removing from storage.' )
                        self.current['path'] = self.sources.github_user.path(self)
                        self.actions.remove(self)
            #else:
                #for repo in self.userStored[owner]:
                    #self.current['software'] = repo
                    #self.debug('del ' + owner + '/' + repo)
                    #self.current['path'] = self.sources.github_user.path(self)
                    #self.actions.remove(self)


    self.sources.github.check(self)
    '''
    path = os.path.join(self.config['STORAGE']['file_path'], 'github_user', user)
    for owner in os.listdir(path):
        self.debug('loop ' + owner)
        target = os.listdir(os.path.join(path, owner))
        for repo in target:
            repo = repo.split('.')
            repo = repo[0]
            self.debug('loop -- ' + repo)
            self.sources.github.check(self)
            #self.checkOne('github', owner, repo, user)
    '''
    return
    self.common.oops()