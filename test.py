### The purpose of this script is to run Relm with a variety of common arguments and conditions that may
### be outside the control of the program, in order to test for correct operation and error handling.

import json, os, shutil, sys
cmdBase = 'python relm.py'

def run(args, notes=''):
    #print('----------')
    run = os.system(cmdBase + ' ' + args)

    print()
    print()
    if run > 0:
        print('Relm failed with arguments: ' + args)
        if (not notes == ''):
            print('notes: ' + notes)
        sys.exit()
    else:
        print('Relm succeeded with arguments: ' + args)
        if (not notes == ''):
            print('notes: ' + notes)
    print('----------')

def update(path):
    if (os.path.isfile(path)):
        with open(path, 'r') as fin:
            data = json.loads(fin.read())
        
        data['version'] = '0.0.1'

        file = open(path,'w')
        file.write(json.dumps(data))
        file.close()

def reset():
    if os.path.exists('.\\releases'):
        try:
            shutil.rmtree('.\\releases')
        except OSError:
            pass

## Begin
pwd = sys.path[0]
os.chdir(pwd)
print('Setting working directory to ' + pwd)
print('----------')

reset()

## Source: GitHub
run('github --add osticket/osticket', 'Standard add')
run('github --add osticket/osticket', 'Add object already in storage')
run('github', 'Standard check')

update(os.path.join('releases', 'github', 'osticket', 'osticket.json'))
run('github', 'Check for updates to artificial version')

run('github --remove osticket/osticket', 'Standard remove')
run('github --remove osticket/osticket', 'Remove object not in storage')
run('github', 'Check empty storage')


## Source: Mozilla
run('mozilla --add firefox', 'Standard add')
run('mozilla --add firefox', 'Add object already in storage')
run('mozilla', 'Standard check')

update(os.path.join('releases', 'mozilla', 'firefox.json'))
run('mozilla', 'Check for updates to artificial version')

run('mozilla --remove firefox', 'Standard remove')
run('mozilla --remove firefox', 'Remove object not in storage')
run('mozilla', 'Check empty storage')
