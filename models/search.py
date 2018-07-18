import os
import re
import sys
from multiprocessing import Process
import time

class Search:
    def __init__(self,term):
        self.term = term

    def search_file(self,dir):
        items_searched = 0
        found = []
        start = time.time()
        for root, dir, files in os.walk(dir, topdown = True):
            for f in files:
                if f.split('.')[0] == self.term:
                    found.append({'term': self.term, 'file': f, 'dir': root})
                items_searched +=1
        print(f'finished in {time.time() - start } found {len(found)} out of {items_searched} items \n\n')

        self.navigate(found)

    def search_directory(self,dir):
        items_searched = 0
        found = []
        start = time.time()
        for root, dir, files in os.walk(dir, topdown = True):
            for d in dir:
                if d == self.term:
                    found.append({'term': self.term, 'file': d, 'dir': root})
                items_searched +=1
        print(f'finished in {time.time() - start } found {len(found)} out of {items_searched} items \n\n')
        self.navigate(found)

    def navigate(self,found):
        navigate = []
        for idx,file in enumerate(found):
            navigate.append({'dir': file['dir'], 'command': idx + 1})
            print(f' {idx + 1} ' + file['file'] + " " + file['dir'])

        inpt = input(' \n Navigate to files? ')

        for f in navigate:
            if f['command'] == int(inpt):
                return os.chdir(f['dir'])
