
## relm.core.config
import configparser, os, sys
#from functions.relm.log import func_log as log

def func_config(self):
    '''
    If config.ini does not exist, create it with default values. Otherwise, load it.

    Arguments:
    self
    '''
    self.debug()

    config = configparser.ConfigParser()
    if os.path.isfile("config.ini"):
        config.sections()
        config.read("config.ini")

        ## Validate read config file
        invalid = False
        if (not config['STORAGE']['type'] in self.storageList):
            self.log('error', 'Invalid storage type specified: ' + config['STORAGE']['type'])
            invalid = True

        if (not config['NOTIFICATIONS']['type'] in self.notificationList):
            self.log('error', 'Invalid notifications type specified: ' + config['NOTIFICATIONS']['type'])
            invalid = True

        if invalid == True:
            sys.exit(1)
    else:
        for x in self.notificationList:
            run = 'self.notification.' + x + '.config(self, config)'
            try:
                config = eval(run) #How to check whether this exist or not
                # Method exists, and was used.  
            except AttributeError:
                pass
                # Method does not exist.  What now?

        for x in self.sourcesList:
            run = 'self.sources.' + x + '.config(self, config)'
            try:
                config = eval(run) #How to check whether this exist or not
                # Method exists, and was used.  
            except AttributeError:
                pass
                # Method does not exist.  What now?

        for x in self.storageList:
            run = 'self.storage.' + x + '.config(self, config)'
            try:
                config = eval(run) #How to check whether this exist or not
                # Method exists, and was used.  
            except AttributeError:
                pass
                # Method does not exist.  What now?

        config["LOGGING"] = {
            "path": "./logs",
            "log_events": "True",
            "log_errors": "True",
            "log_warnings": "True"
        }
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    return config
    
'''
for x in self.notificationList:
    run = 'self.notification.' + x + '.config(self, config)'
    config = eval(run)

for x in self.sourcesList:
    run = 'self.sources.' + x + '.config(self, config)'
    config = eval(run)

for x in self.storageList:
    run = 'self.storage.' + x + '.config(self, config)'
    config = eval(run)
'''

'''
#config['STORAGE'] = { "type": "file",
#                    "file_path": "./releases" }


config["GITHUB"] = { "token": "" }
config["NOTIFICATIONS"] = {    "type": "email",
                                    "email_host": "smtp.domain.com",
                                    "email_to": "example@domain.com",
                                    "email_from": "example@domain.com",
                                    "email_password": "BadPassword"}
'''