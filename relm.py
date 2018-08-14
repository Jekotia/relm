from argparse import ArgumentParser
import configparser
import datetime
import json
import requests
import os.path
import os
import re
import smtplib
from string import Template
from subprocess import call
import sys

pwd = sys.path[0]
os.chdir(pwd)
print('Setting working directory to ' + pwd)

def oops():
    print('    ┬─┬ ┌(°-°┌) ┬─┬')
    print()
    print('    ┬─┬ (┐°-°)┐ ┬─┬')
    print()
    print('┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻')
    print()
    print('┻━┻    (ಠ ∩ ಠ)   ┻━┻')
    print()
    print('Something has gone horribly wrong. Please inform the developer.')
    sys.exit()

def jsonPrint(data):
    print(json.dumps(data))

def getOwner(data):
    myString = data.split("/")
    owner = myString[0]
    return owner #print("owner=" + owner)

def getRepo(data):
    myString = data.split("/")
    repo = myString[1]
    return repo #print("repo=" + repo)


class relmon():
    action = False
    args = {}
    config = {}
    source = ""
    user = False
    userStarred = {}
    userStored = {}
    GitHub_Auth_Header = {}
    def __init__(self, args):
        self.args = args

        self.config = configparser.ConfigParser()

        if os.path.isfile("config.ini"):
            self.config.sections()
            self.config.read("config.ini")

            if (not self.config['STORAGE']['type'] == "file"):
                self.log('error', 'Invalid storage type specified: ' + self.config['STORAGE']['path'])
                sys.exit()
        else:
            self.config['STORAGE'] = { "type": "file",
                                "path": "./releases" }
            self.config["GITHUB"] = { "token": "" }
            self.config["NOTIFICATIONS"] = {    "type": "email",
                                                "email_host": "smtp.domain.com",
                                                "email_port": "25",
                                                "email_secure": False,
                                                "email_to": "example@domain.com",
                                                "email_from": "example@domain.com",
                                                "email_password": "BadPassword"}
            self.config["LOGGING"] = {  "path": "./logs",
                                        "log_events": "True" }
            with open("config.ini", "w") as configfile:
                self.config.write(configfile)

        if self.config['GITHUB']['token'] == '':
            self.GitHub_Auth_Header = { }
        else:
            self.GitHub_Auth_Header = { 'Authorization': 'token ' + self.config['GITHUB']['token'] }

        sources = ['mozilla','github','github-user']
        for target in sources:
            path = os.path.join(self.config['STORAGE']['path'], target)
            if not os.path.exists(path):
                os.makedirs(path)

        if not os.path.isfile('email.template'):

            templateData = '''From: $sender
To: $to
Subject: RELMON $name has been updated
Mime-Version: 1.0
Content-Type: text/html

Monitored software <strong>$name</strong> has been updated from version <strong>$version_old</strong> to version <strong>$version_new</strong>.
<br/>
You can find more information <a href="$url">here</a>.'''

            with open('email.template', 'w') as templatefile:
                templatefile.write(templateData)
    
    def debug(self, msg):
        if self.args.verbose:
            print("DEBUG:   " + msg)

    def log(self, kind, msg):
        print(kind.upper() + ": " + msg)

        path = self.config['LOGGING']['path']
        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(path, kind + ".log")

        msg = str(datetime.datetime.now()) + "   " + msg + "\n"

        if (kind == 'event' and self.config['LOGGING'].getboolean('log_events')) or kind == 'error':
            with open(path, 'a') as logfile:
                logfile.write(msg)

    def add(self, source=False, developer=False, software=False, user=False):
        if (source == 'github') and (not user == False):
            msg = developer + '/' + software
        elif self.source == 'github':
            developer = getOwner(self.args.add)
            software = getRepo(self.args.add)
            msg = developer + '/' + software
        elif self.source == 'mozilla':
            developer = self.args.source
            software = self.args.add
            msg = software

        if self.config['STORAGE']['type'] == 'file':
            ##
            if not self.storageRead(source, developer, software, user):
                query = self.query(source, developer, software, user)
                if (query == False):
                    return False
                else:
                    latest = self.convert(self.source, developer, software, query)
            elif (source == 'github') and (not user == False):
                print(developer + '/' + software + ' is already in storage for source \'github\', user \'' + user + '\'')
                return
            elif self.source == 'github':
                print(developer + '/' + software + ' is already in storage for source \'github\'')
                sys.exit()
            else:
                print(software + ' is already in storage for source \'' + self.source + '\'')
                sys.exit()

            if self.storageWrite(self.source, developer, software, latest, user):
                usrmsg = ''
                if (not user == False):
                    usrmsg = ', for user \'' + user + '\''
                self.log('event', 'Added ' + msg + ' to storage for source \'' + self.source + '\'' + usrmsg)
                    #self.storageWrite(self.args.source, developer, software, apiResult)

    def remove(self, source=False, developer=False, software=False, user=False):
        if self.source == 'github':
            if (user == False):
                developer = getOwner(self.args.remove)
                software = getRepo(self.args.remove)
        elif self.source == 'mozilla':
            developer = self.args.source
            software = self.args.remove

        if self.config['STORAGE']['type'] == 'file':
            if (source == 'github') and (not user == False):
                dirPath = os.path.join(self.config['STORAGE']['path'], 'github-user', user, developer)
                filePath = os.path.join(dirPath, software + '.json')
                msg = developer + '/' + software
            elif self.source == 'github':
                dirPath = os.path.join(self.config['STORAGE']['path'], self.source, developer)
                filePath = os.path.join(dirPath, software + '.json')
                msg = developer + '/' + software
            else:
                dirPath = os.path.join(self.config['STORAGE']['path'], self.source)
                filePath = os.path.join(dirPath, software + '.json')
                msg = software

            if os.path.exists(filePath):
                try:
                    os.remove(filePath)
                except:
                    self.log('error', 'Failed to remove ' + msg + ' from storage for \'' + self.source + '\'')
                else:
                    self.log('event', 'Removed \'' + msg + '\' from storage for \'' + self.source + '\'')
                    if len(os.listdir(dirPath) ) == 0:
                        try:
                            os.rmdir(dirPath)
                        except:
                            self.log('error', 'Failed to remove empty directory: ' + dirPath)
                        else:
                            self.log('event', 'Removed empty directory: ' + dirPath)
            else:
                print('No such item to remove: ' + filePath)

    def check(self, source, user=False):
        self.debug('relmon.check: source = ' + source)
        if source == 'all':
            path = os.path.join(self.config['STORAGE']['path'], 'github-user')
            for folder in os.listdir(path):
                self.debug('checking github user ' + folder)
                self.check('github', folder)
            self.check('github')
            self.check('mozilla')
        else:
            self.debug('relmon.check: Checking for new releases in storage for ' + source)
            if (self.config['STORAGE']['type'] == 'file'):
                if (not user == False):
                    self.debug('relmon.check: user = ' + user)
                    path = os.path.join(self.config['STORAGE']['path'], 'github-user', user)
                    if not os.path.exists(path):
                        os.makedirs(path)
                else:
                    path = os.path.join(self.config['STORAGE']['path'], source)
                if (os.path.exists(path)):
                    if (source == 'github') and (not user == False):
                        self.debug("relmon.check: user = " + user)
                        self.query_github_user(user)
                    elif (source == 'github'):
                        for developer in os.listdir(path):
                            self.debug('relmon.check: loop ' + developer)
                            target = os.listdir(os.path.join(path, developer))
                            for software in target:
                                software = software.split('.')
                                software = software[0]
                                self.debug('relmon.check: loop -- ' + software)
                                self.checkOne(source, developer, software)
                    elif source == 'mozilla':
                        self.debug('relmon.check: loop ' + source)
                        for software in os.listdir(path):
                            software = software.split('.')
                            software = software[0]
                            self.debug('relmon.check: loop -- ' + software)
                            self.checkOne(source, source, software)
                else:
                    self.log('error', 'Storage of type "file" for source ' + source + ' does not exist')
                    self.debug(path)

    def checkOne(self, source, developer, software, user=False):
        ## Make an API query
        query = self.query(source, developer, software)
        ## Convert the API query data into the value pairs we use
        apiResult = self.convert(source, developer, software, query)
        storageResult = self.storageRead(source, developer, software, user)

        ## Check if the software in question is in storage
        if not storageResult == False:
            latest = self.compare(storageResult['version'], apiResult['version'], apiResult)
            if latest['status'] == "updated":
                if self.notify(latest, storageResult):
                    self.storageWrite(source, developer, software, latest, user)
            self.debug(json.dumps(latest))
        #else:
        #    pass
        #    self.storageWrite(source, developer, software, apiResult, user)

    def compare(self, storageData, apiData, json):
        updated = False
        sVer = storageData.split(".")
        aVer = apiData.split(".")

        y = 0
        while y < len(aVer):
            #self.debug("aVer[" + str(y) + "]: " + aVer[y])
            #self.debug("sVer[" + str(y) + "]: " + sVer[y])
            if int(aVer[y]) > int(sVer[y]):
                self.debug("NEW RELEASE")
                updated = True
                break
            y = y + 1

        if updated:
            json['status'] = "updated"
        else:
            json['status'] = "not-updated"
        return json

    def convert(self, source, developer, software, data):
        '''
        {
        "checked_at": "2018-07-12T00:02:23",
        "status": null,
        "developer": "44670",
        "software": "NTRViewer",
        "version": null,
        "url": null,
        "type": "release"
        }
        '''

        releaseStatus = None
        releaseDeveloper = developer
        releaseSoftware = software

        if source == 'github':
            #print(data)
            if 'tag_name' in data:
                releaseType = 'release'
                releaseVersion = re.sub('[-a-zA-Z]', '', str(data['tag_name']))
                releaseURL = str(data['html_url'])
            elif 'name' in data:
                releaseType = 'tag'
                releaseVersion = re.sub('[-a-zA-Z]', '', str(data['name']))
                releaseURL = 'https://github.com/' + developer + '/' + software + '/releases/tag/' + str(data['name'])
    
        elif source == 'mozilla':
            releaseType = None
            releaseVersion = str(data['LATEST_' + software.upper() + '_VERSION'])
            releaseURL = 'https://www.mozilla.org/en-US/' + software + '/' + releaseVersion + '/releasenotes/'
            #self.debug('relmon.convert: releaseURL = ' + releaseURL)

        releaseDict = { 'status': releaseStatus,
                        'developer': releaseDeveloper,
                        'software': releaseSoftware,
                        'version': releaseVersion,
                        'url': releaseURL,
                        'type': releaseType
                        }
        return releaseDict

    def notify(self, jsonNew, jsonOld):
        self.debug("NOTIFYING ABOUT NEW RELEASE")
        if self.config['NOTIFICATIONS']['type'] == 'email':

            fromaddr = self.config['NOTIFICATIONS']['email_from']
            toaddrs  = self.config['NOTIFICATIONS']['email_to']

            with open('./email.template', 'r') as tpl:
                tpl = tpl.read()

            template = Template(tpl).safe_substitute(sender=fromaddr, to=toaddrs, name=jsonNew['software'], version_old=jsonOld['version'], version_new=jsonNew['version'], url=jsonNew['url'])

            msg = template

            try:
                email_host = self.config['NOTIFICATIONS']['email_host']
                email_port = self.config['NOTIFICATIONS']['email_port']
                email_user = self.config['NOTIFICATIONS']['email_from']
                email_pass = self.config['NOTIFICATIONS']['email_password']
                email_secure = self.config['NOTIFICATIONS'].getboolean('email_secure')

                if email_secure == True:
                    self.debug("Using secure SMTP connection")
                    server_ssl = smtplib.SMTP_SSL(email_host, email_port)
                    if verbose == True:
                        server_ssl.set_debuglevel(1)

                    server_ssl.ehlo()
                    #server_ssl.starttls()
                    server_ssl.login(email_user, email_pass)
                    server_ssl.sendmail(fromaddr, toaddrs, msg)
                    server_ssl.close()

                else:
                    self.debug("Using insecure SMTP connection")
                    server = smtplib.SMTP(email_host, email_port)
                    if verbose == True:
                        server.set_debuglevel(1)

                    server.ehlo()
                    server.login(email_user, email_pass)
                    server.sendmail(fromaddr, toaddrs, msg)
                    server.close()
            except smtplib.SMTPAuthenticationError:
                pass
                self.log("error", "Failed to send email notification for " + jsonNew['developer'] + " " + jsonNew['software'])
                status = False
            else:
                self.log("event", "Successfully sent email notification for " + jsonNew['developer'] + " " + jsonNew['software'])
                status = True
            return status

    def query(self, source, developer, software, user=False):
        self.debug('relmon.query: source = ' + source)
        if source == 'github':
            query = self.query_github('releases', source, developer, software)
            if query == False:
                print('Could not find releases for ' + developer + '/' + software + 'on github. Will try tags')
                query = self.query_github('tags', source, developer, software)
                if query == False:
                    self.log('error', 'Could not find releases or tags for ' + developer + '/' + software + ' on GitHub')
                    return False
                elif not any(char.isdigit() for char in query['name']):
                    print('Cannot work with non-numerical version in ' + developer + '/' + software)
                    return False
                else:
                    print('Using tags for ' + developer + '/' + software)
                    return query
            elif not any(char.isdigit() for char in query['tag_name']):
                print('Cannot work with non-numerical version in ' + developer + '/' + software)
                return False
            else:
                return query
        elif source == 'mozilla':
            query = self.query_mozilla(software)
            return query
        else: oops()
        return False

    def query_get(self, url, headers={}):
        result = requests.get(url, headers=headers)
        return result

    def query_github(self, kind, source, developer, software, user=False):
        url='https://api.github.com/repos/' + developer + '/' + software + '/' + kind
        self.debug('API URL: ' + url)
        query = self.query_get(url, headers=self.GitHub_Auth_Header)
        jsonQuery = json.loads(query.text)

        if json.dumps(jsonQuery) == '[]':
            return False
        #sys.exit()
        for jsonEntry in jsonQuery:
            break
        return jsonEntry

    def query_github_user(self, user):
        ## Assemble list of starred repos
        url = 'https://api.github.com/users/' + user + '/starred?per_page=100'
        self.debug('API URL: ' + url)
        query = self.query_get(url, headers=self.GitHub_Auth_Header )
        jsonQuery = json.loads(query.text)

        for jsonEntry in jsonQuery:
            owner = jsonEntry['owner']['login']
            repo = jsonEntry['name']

            if not owner in self.userStarred:
                self.userStarred[owner] = []

            self.userStarred[owner].append(repo)

        ## Assemble list of stored repos
        if (self.config['STORAGE']['type'] == 'file'):
            path = os.path.join(self.config['STORAGE']['path'], 'github-user', user)

            if (not os.path.exists(path)):
                self.debug('relmon.query_github_user: ' + path + ' does not exist. Will attempt to create')
                try:
                    os.makedirs(path)
                except:
                    self.log('error', path + ' does not exist and could not be created')
                    return False
            else:
                self.debug('relmon.query_github_user: ' + path + ' exists')

            for owner in os.listdir(path):
                if not owner in self.userStored:
                    self.userStored[owner] = []

                target = os.listdir(os.path.join(path, owner))
                for repo in target:
                    repo = repo.split('.')
                    repo = repo[0]
                    self.userStored[owner].append(repo)
        else: oops()


        for owner in self.userStored:
            if owner in self.userStarred:
                for repo in self.userStored[owner]:
                    if repo in self.userStarred[owner]:
                        pass ; self.debug('keep ' + owner + '/' + repo)
                    else:
                        self.debug('del ' + owner + '/' + repo)
                        self.log('event', '\'' + owner + '/' + repo + '\' found in storage for github user \'' + user + '\', but not in the users starred repos. Removing from storage.' )
                        self.remove('github', owner, repo, user)
            else:
                for repo in self.userStored[owner]:
                    self.debug('del ' + owner + '/' + repo)
                    self.remove('github', owner, repo, user)

        ## Ensure everything in self.userStarred is in storage
        for owner in self.userStarred:
            self.debug('relmon.query_github_user: owner = ' + owner)
            for repo in self.userStarred[owner]:
                self.debug('relmon.query_github_user: repo = ' + repo)
                self.add('github', owner, repo, user)
                #query = self.query('github', owner, repo)

        path = os.path.join(self.config['STORAGE']['path'], 'github-user', user)
        for owner in os.listdir(path):
            self.debug('relmon.query_github_user: loop ' + owner)
            target = os.listdir(os.path.join(path, owner))
            for repo in target:
                repo = repo.split('.')
                repo = repo[0]
                self.debug('relmon.check: loop -- ' + repo)
                self.checkOne('github', owner, repo, user)

    def query_mozilla(self, software):
        url = 'https://product-details.mozilla.org/1.0/' + software.lower() + '_versions.json'
        self.debug('API URL: ' + url)

        query = self.query_get(url)
        jsonQuery = json.loads(query.text)
        return jsonQuery

    def storageRead(self, source, developer, software, user=False):
        if (self.config['STORAGE']['type'] == 'file'):
            if (source == 'github') and (not user == False):
                path = os.path.join(self.config['STORAGE']['path'], 'github-user', user, developer, software + '.json')
            elif (source == 'github'):
                path = os.path.join(self.config['STORAGE']['path'], source, developer, software + '.json')
            elif (source == 'mozilla'):
                path = os.path.join(self.config['STORAGE']['path'], source, software + '.json')

            self.debug('Storage file path: ' + path)
            if (os.path.isfile(path)):
                with open(path, 'r') as fin:
                    self.debug('Found in storage')
                    return json.loads(fin.read())
            else:
                self.debug('Not found in storage')
                return False
        else: oops()

    def storageWrite(self, source, developer, software, data, user=False):
        if self.config['STORAGE']['type'] == 'file':
            if (source == 'github') and (not user == False):
                path = os.path.join(self.config['STORAGE']['path'], 'github-user', user, developer)
            elif (source == 'github'):
                path = os.path.join(self.config['STORAGE']['path'], source, developer)
            elif (source == 'mozilla'):
                path = os.path.join(self.config['STORAGE']['path'], source)



            if not os.path.exists(path):
                self.debug('relmon.storageWrite: ' + path + ' does not exist. Will attempt to create')
                try:
                    os.makedirs(path)
                except:
                    self.log('error', path + ' does not exist and could not be created')
                    return False
            else:
                self.debug('relmon.storageWrite: ' + path + ' exists')

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

    def validateArgs(self):
        self.debug('source = ' + self.args.source)

        if self.args.source == 'all':
            self.action = 'check-all'
            self.source = 'all'
        ## source = github
        elif (self.args.source == 'github') or (self.args.source == 'mozilla'):
            self.source = self.args.source
            if (self.args.source == 'github') and (not self.args.user == False):
                self.action = 'user'
            elif (not self.args.add == False):
                self.action = 'add'
            elif (not self.args.remove == False):
                self.action = 'remove'
            else:
                self.action = 'check'

        self.debug('action = ' + self.action)
        return self.action


parser = ArgumentParser(prog='relm.py')
parser.add_argument('source', choices=['all','github','mozilla'], default=False, help='The source to use')

parserGroup = parser.add_mutually_exclusive_group()
parserGroup.add_argument('--add','-a', dest='add', default=False, help='Add a piece of software to storage')
parserGroup.add_argument('--remove','-r', dest='remove', default=False, help='Remove a piece of software from storage')
parserGroup.add_argument('--user','-u', dest='user', default=False, help='User account for services like Github')


parser.add_argument('--debug','-d', dest='verbose', action='store_true', default=False, help='Show debugging statements in output')
args = parser.parse_args()

runtime = relmon(args)

verbose = args.verbose

if not runtime.validateArgs() == False:
    if (runtime.action == 'check') or (runtime.action == 'check-all'):
        runtime.check(runtime.source)
    elif runtime.action == 'add':
        runtime.add(runtime.args.source)
    elif runtime.action == 'remove':
        runtime.remove(runtime.args.source)
    elif runtime.action == 'user':
        runtime.check(runtime.source, runtime.args.user)
