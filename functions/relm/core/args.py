## relm.core.args
from argparse import ArgumentParser

def func_args(self):
    #self.debug()

    parser = ArgumentParser(prog='relm.py')
    parser.add_argument('source', choices=['all','github','mozilla'], default=False, help='The source to use')

    parserGroup = parser.add_mutually_exclusive_group()
    parserGroup.add_argument('--add','-a', dest='add', default=False, help='Add a piece of software to storage')
    parserGroup.add_argument('--remove','-r', dest='remove', default=False, help='Remove a piece of software from storage')
    parserGroup.add_argument('--user','-u', dest='user', default=False, help='User account for services like Github')


    parser.add_argument('--debug','-d', dest='verbose', action='store_true', default=False, help='Show debugging statements in output')
    
    self.args = parser.parse_args()
    
    self.verbose = self.args.verbose
    self.debug()

    return self.args
