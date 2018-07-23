import os
from database.database import Database

from utils.stack import Stack
from utils.functions import add_occurences, check_file_format




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

        self.menu_choices = [
            {'command': 'previous_directory', 'hotkey': 'b', 'menu_action': self.previous_dir},
            {'command': 'view_all_files', 'hotkey': 'v', 'menu_action': self.list_directory, 'menu_action_arg': 'list_files'},
            {'command': 'view_all_directories', 'hotkey': 'd', 'menu_action': self.list_directory, 'menu_action_arg': 'list_directories'},
            {'command': 'run_file', 'hotkey': 'r', 'menu_action': self.run_file},
            {'command': 'open_project', 'hotkey': 'o', 'menu_action': self.open_dir_atom},
            {'command': 'custom_command', 'hotkey': 'c', 'menu_action': self.custom_command},
            {'command': 'quick_navigation', 'hotkey': 'q', 'menu_action': self.quick_nav},
            {'command': 'help', 'hotkey': '--help', 'menu_action': self.help}
            ]


        #starts system by listing current directory with all contents
        self.list_directory('list_all')



    def __repr__(self):
        return f"<Navigator with {self.dirs} directories and {self.files} files>"

    def menu(self):

        """

        Calls different functions based on user input

        """




        print(f' \n\n {os.getcwd()} \n\n')
        selection = input('')
        try:
            #loop through menu choices, if hotkey = input selection run the coresponding function or if input is an integer change the directory
            #otherwise raise an error
            for choice in self.menu_choices:
                if choice['hotkey'] == selection:
                    menu_action = choice.get('menu_action')
                    menu_action_arg = choice.get('menu_action_arg')
                    if menu_action_arg is not None:
                        menu_action(menu_action_arg)
                    else:
                        menu_action()
            if isinstance(int(selection),int):
                self.change_dir(selection)
            else:
                raise ValueError('Please Enter Valid Menu Choice, --help')
        except ValueError as err:
            print('Please Enter Valid Menu Choice --help')
            self.menu()


    def list_directory(self,display):


        """
        List all directories and files in the current directory.

        @param display: displays which type of data gets appended and output

        """
        self.clear_terminal()
        self.dirs = []
        self.files = []

        directory_list = os.listdir(os.getcwd())

        if display == "list_all":
            for idx, item in enumerate(directory_list):
                if os.path.isfile(item):
                    print(f' FILE {idx + 1} ' + item)
                    self.files.append({'file': item, 'command': idx + 1})
                if os.path.isdir(item):
                    print(f' DIR {idx + 1} ' + item)
                    self.dirs.append({'dir': os.getcwd() + '\\' + item, 'command': idx + 1})

        elif display == "list_files":
            for idx, file in enumerate(directory_list):
                if os.path.isfile(file):
                    print(f' FILE {idx + 1} ' + file)
                    self.files.append({'file': file, 'command': idx + 1})

        elif display == "list_directories":
            for idx, dir in enumerate(directory_list):
                if os.path.isdir(dir):
                    print(f' DIR {idx + 1} ' + dir)
                    self.dirs.append({'dir': os.getcwd() + '\\' + dir, 'command': idx + 1})

        self.menu()

    def run_file(self):
        """

        checks file type and excutes in a seprate terminal instance and saves URL stack to db


        """
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


    def change_dir(self,selection):
        """
        changes the current directory based on user input

        @param selection: user input provided

        """
        for d in self.dirs:
            if d['command'] == int(selection):
                os.chdir(d['dir'])
                stack.push(d['dir'])
                break
        self.list_directory('list_all')

    def previous_dir(self):
        """
        moves back 1 directory and pops first one off the stack

        """
        try:
            #changes dir to second position in stack (previous dir)
            os.chdir(stack.position(1))
            #remove first directory from stack after navigating
            stack.pop()
            self.list_directory('list_all')
        except IndexError:
            self.list_directory('list_all')
            print('No Directory History')


    def custom_command(self):
        """
        asks user for input then excutes command

        """
        command = input('enter command: \n')
        os.system(command)
        if input('enter another command? (y/n) \n') == "y":
            self.custom_command()
        else:
            print('custom command mode exited')
            self.menu()

    def quick_nav(self):

        """
        queries the database and sorts saved filepath data by most used.

        """

        self.clear_terminal()
        #get all routes
        #all all occurences of routes
        routes = add_occurences([{'route': i['route'][0], 'id': i['_id']} for i in Database.find('routes',{})])

        count = lambda i: list(i.values())
        #sort by decending
        descend_by_count = sorted(count(routes), key = lambda i: i['count'], reverse=True)

        choices = []
        for idx, route in enumerate(descend_by_count):
            print(' ' + str(idx + 1) + ' ' + route['route'])
            choices.append({'idx': idx, 'route': route['route'], 'id': route['id']})

        selection = input(' \n\n enter number: ')
        for choice in choices:
            try:
                if choice['idx'] + 1 == int(selection):
                    os.chdir(choice['route'])
                    stack.push(choice['route'])
                    self.clear_terminal()
                    self.list_directory('list_all')
                    self.menu()
            except FileNotFoundError:
                self.clear_terminal()
                print(' \n\n file was not found, perhaps it was moved. \n\n')
                to_delete = input(' Would you like to delete the path? (y/n) ')
                if to_delete == "y":
                    Database.remove('routes', {'_id': choice['id']})
                    print(' \n\n path removed')

        self.menu()



    def clear_terminal(self):

        """

        clears terminal output

        @returns function or None

        """

        if self.debug:
            return None
        return os.system('cls')


    def help(self):

        """

        Prints out menu options


        """
        self.clear_terminal()
        for option in self.menu_choices:
            print(f" command: {option['command']} ---> hotkey: {option['hotkey']}")
        self.menu()
