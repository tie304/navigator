import os
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE
from database.database import Database

from utils.stack import Stack
from utils.functions import add_occurences, check_file_format
from models.search import Search


#create a stack to hold directories visited and add the current directory
stack = Stack()
#push current working directory into the stack
stack.push(os.getcwd())

class Navigator:

    def __init__(self):
        #holds all of the working directories
        self.dirs = []
        #holds all of the working files
        self.files = []
        #stops clear feature so traceback can be viewed
        self.debug = False
        #starts system by listing current directory
        self.list_all()


    def __repr__(self):
        return f"<Navigator with {self.dirs} directories and {self.files} files>"

    def menu(self):
        try:
            choice = input(f' \n Curent Directory: {os.getcwd()} \n \n 1: View all files (v) \n 2: View all Directories (d) \n 3: Quick Nav (q) \n 4. Back directory (b) \n 5. Run File (r) \n 6. Custom Command (c) \n 7. Search (s) \n 8. Open Project (o) \n \n' )
            if choice == "b":
                self.previous_dir()
            elif choice == "v":
                self.list_files()
            elif choice == "d":
                self.list_dir()
            elif choice == "r":
                self.run_file()
            elif choice == "o":
                self.open_dir_atom()
            elif choice == "c":
                self.custom_command()
            elif choice == "q":
                self.quick_nav()
            elif choice == "s":
                self.search()
            elif int(choice):
                self.change_dir(choice)
            else:
                raise ValueError('please enter a valid menu choice')
        except ValueError:
            self.clear()
            print('please enter a valid menu choice')
            self.menu()

    def list_all(self):
        self.clear()
        self.dirs = []
        self.files = []
        current_dir = os.listdir(os.getcwd())
        for idx,e in enumerate(current_dir):
            if os.path.isfile(e):
                print(f' FILE {idx + 1} ' + e)
                self.files.append({'file': e, 'command': idx + 1})
            if os.path.isdir(e):
                print(f' DIR {idx + 1} ' + e)
                self.dirs.append({'dir': os.getcwd() + '\\' + e, 'command': idx + 1})
        self.menu()


    def list_dir(self):
        self.clear()
        self.dirs = []
        current_dir = os.getcwd()
        dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
        for idx, d in enumerate(dirs):
            self.dirs.append({'dir':current_dir + '\\' + d, 'command': idx + 1})
            print(f' DIR {idx + 1} ' + d)
        self.menu()

    def list_files(self):
        self.clear()
        self.files = []
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for idx, f in enumerate(files):
            self.files.append({'file': f, 'command': idx + 1})
            print(f' FILE {idx + 1} ' + f)
        self.menu()

    def run_file(self):
        input_num = input('Run File Number: ')
        for f in self.files:
            if f['command'] == int(input_num):
                os.system(f"start cmd /K {check_file_format(f['file'], os.getcwd())}")
                break
        stack.save_to_db()
        self.menu()

    def open_dir_atom(self):
        input_num = input('Open Project Number: ')
        for d in self.dirs:
            if d['command'] == int(input_num):
                os.chdir(d['dir'])
                os.system('atom .')
                break
        stack.save_to_db()
        self.menu()


    def change_dir(self,choice):
        for d in self.dirs:
            if d['command'] == int(choice):
                os.chdir(d['dir'])
                stack.push(d['dir'])
                break
        self.list_all()

    def previous_dir(self):
        try:
            print(stack.items)
            os.chdir(stack.first())
            stack.pop()
            self.list_all()
        except IndexError:
            print('No Directory History')
            self.list_all()

    def custom_command(self):
        command = input()
        os.system(command)
        self.menu()

    def quick_nav(self):

        self.clear()
        #get all routes
        #all all occurences of routes
        data = add_occurences([{'route': i['route'][0], 'id': i['_id']} for i in Database.find('routes',{})])
        #sort by decending
        count = lambda i: list(i.values())

        decending = sorted(count(data), key = lambda i: i['count'], reverse=True)

        choices = []
        for idx, e in enumerate(decending):
            print(' ' + str(idx + 1) + ' ' + e['route'])
            choices.append({'idx': idx, 'route': e['route'], 'id': e['id']})

        choice = input(' \n\n enter number: ')
        for e in choices:
            try:
                if e['idx'] + 1 == int(choice):
                    print(e['route'])
                    os.chdir(e['route'])
                    stack.push(e['route'])
            except FileNotFoundError:
                self.clear()
                print(' \n\n file was not found, perhaps it was moved. \n\n')
                to_delete = input(' Would you like to delete the path? (y/n) ')
                if to_delete == "y":
                    Database.remove('routes', {'_id': e['id']})
                    print(' \n\n path removed')

        self.menu()


    def search(self):
        self.clear()
        nav = input(' 1. Search Files (f) \n 2. Search Dirs (d) \n 3. Search file contents \n')

        if nav == "f":
            query = input(' Search for filename: ')
            Search(query).search_file(os.getcwd())
        elif nav == "d":
            query = input(' Search for directory: ')
            Search(query).search_directory(os.getcwd())

        self.menu()

    def clear(self):
        if self.debug:
            return None
        return os.system('cls')
