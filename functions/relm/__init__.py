
## relm.__init__
import os, sys

class relm():
    import functions.relm.core as core #import functions.relm.core as core

#    from functions.relm. import func_ as
    from functions.relm.compare import func_compare as compare
    #from functions.relm.debug import func_debug as debug
    from functions.relm.log import func_log as log
    from functions.relm.validateArgs import func_validateArgs as validateArgs

    import functions.relm.actions as actions
    import functions.relm.notification as notification
        #import functions.relm.query as query
    import functions.relm.sources as sources
    import functions.relm.storage as storage
    from functions.common import debug
    from functions.common import info
    import functions.common as common

    action = False
    args = {}
    config = {}
    current = {
        'action': '',
        'source': '',
        'developer': '',
        'software': '',
        'user': False,
        'path': '',
        'body': ''
    }

    source = ''

    sourcesList = []
    storageList = []
    notificationList = []

    userStarred = {}
    userStored = {}

    verbose = False

    def __init__(self):
        self.args = relm.core.args(self) # self.core.args(self)
        self.debug()

        def loadList(self, target):
            '''
            Create list of directories within the target.

            Arguments:
            self
            target -- target directory to iterate over.
            '''
            myList = []
            for x in os.listdir(target):
                if (not x == '__pycache__'):
                    dir = os.path.join(target, x)
                    if os.path.isdir(dir):
                        myList.append(x)
                    
            return myList

            #run = 'self.debug("' + name + ' = " + str(self.' + name + '))'
            #eval(run)

        path = os.path.join(sys.path[0], 'functions', 'relm', 'storage')
        self.storageList = loadList(self, path)
        self.debug('storageList = ' + str(self.storageList))

        path = os.path.join(sys.path[0], 'functions', 'relm', 'sources')
        self.sourcesList = loadList(self, path)
        self.debug('sourcesList = ' + str(self.sourcesList))

        path = os.path.join(sys.path[0], 'functions', 'relm', 'notification')
        self.notificationList = loadList(self, path)
        self.debug('notificationList = ' + str(self.notificationList))

        self.config = relm.core.config(self) # self.core.config(self)
        self.debug()
        self.validateArgs()
        self.debug()

        '''
        path = os.path.join(sys.path[0], 'functions', 'relm', 'sources')
        print(path)
        for x in os.listdir(path):
            if (not x == '__pycache__'):
                dir = os.path.join(path, x)
                if os.path.isdir(dir):
                    self.sourcesList.append(x)
        self.debug('sourcesList = ' + str(self.sourcesList))

        path = os.path.join(sys.path[0], 'functions', 'relm', 'storage')
        print(path)
        for x in os.listdir(path):
            if (not x == '__pycache__'):
                dir = os.path.join(path, x)
                if os.path.isdir(dir):
                    self.storageList.append(x)
        self.debug('storageList = ' + str(self.storageList))
        '''


#        sources = ['mozilla','github','github-user']
#        for target in sources:
#            path = os.path.join(self.config['STORAGE']['file_path'], target)
#            if not os.path.exists(path):
#                os.makedirs(path)
