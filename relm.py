## Standard Library
import os, sys

## Custom
import functions.common as common
from functions.relm import relm

## Begin
pwd = sys.path[0]
os.chdir(pwd)
#relm.info('Setting working directory to ' + pwd)

def dictConfig(config):
    pass


runtime = relm()
runtime.debug()

dictConfig(runtime.config)


if (runtime.action == 'check') or (runtime.action == 'check-all'):
    runtime.sources.check(runtime) #runtime.actions.check(runtime)
    runtime.debug()
#elif (runtime.action == 'add') or (runtime.action == 'remove'):
#    runtime.current['source'] = runtime.args.source
elif (runtime.action == 'user'):
    runtime.current['user'] = runtime.args.user
    runtime.sources.check(runtime)
elif (runtime.action == 'add') or (runtime.action == 'remove'):
    runtime.current['action'] = runtime.action
    runtime.current['source'] = runtime.args.source



    if runtime.args.source == 'github':
        if (not runtime.args.add == False):
            target = runtime.args.add
        if (not runtime.args.remove == False):
            target = runtime.args.remove

        #run = 'runtime.sources.' + runtime.args.source + '.'
        #runtime.current['developer'] = eval(run)
        runtime.current['developer'] = runtime.sources.developer(runtime, target)
        runtime.debug()
        runtime.current['software'] = runtime.sources.software(runtime, target)
        runtime.debug()
    else: #elif runtime.args.source == 'mozilla':
        runtime.current['developer'] = runtime.args.source
        run = 'runtime.args.' + runtime.action
        runtime.current['software'] = eval(run)
        runtime.debug()

    run = 'runtime.sources.' + runtime.current['source'] + '.path(runtime)'
    runtime.current['path'] = eval(run)
    runtime.debug()

    run = 'runtime.actions.' + runtime.action + '(runtime)'
    eval(run)
    runtime.debug()
    
elif runtime.action == 'remove':
    runtime.actions.remove('')
    runtime.debug()
elif runtime.action == 'user':
    #runtime.actions.check(runtime.args.source, runtime.args.user)
    runtime.debug()

sys.exit(0)
if (runtime.args.add == False) and (runtime.args.remove == False):
    runtime.sources.check(runtime)
    runtime.debug()
elif (not runtime.args.add == False):
    runtime.actions.add(runtime)
    runtime.debug()
elif (not runtime.args.remove == False):
    runtime.actions.remove(runtime)
    runtime.debug()