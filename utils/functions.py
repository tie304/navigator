import os
import json
from pathlib import Path



def add_occurences(lst):

    """

    adds number of occurences of routes coming from the database

    @param lst: list of dicts containing URLs from the database

    @returns: Dictionary

    """
    items = {}
    for idx, item in enumerate(lst):
        if item['route'] not in items:
            items[item['route']] = {'route': item['route'], 'count': 1, 'id': item['id']}
        else:
            items[item['route']]['count'] += 1
    return items



def check_file_format(file,dirc):

    """

    returns format of a file only .js and .py supported at this time

    @param file: Filename in question

    @param dirc: Directory in which the file is located

    @returns: String

    """

    if file.endswith('.py'):
        return f'python {file}'
    if file.endswith('.js'):
        return run_node_file(dirc,file)


def run_node_file(dirc,file):
    """

    Checks if theres a package.json in directory if there is, run the npm start command otherwise run node {filename} in question

    @param dirc: Directory in which file is located

    @param file: Javascript file in question

    @returns: String


    """
    os.listdir(dirc)
    package = Path(f'{dirc}\\package.json')
    if package.is_file():
        with open(f'{dirc}\\package.json') as data_file:
            data = json.load(data_file)
            try:
                if data['scripts']['start']:
                    return 'npm run start'
            except KeyError:
                return f'node {file}'
    else:
        return f'node {file}'
