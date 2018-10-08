import os
import re
from collections import defaultdict


# GLOBAL VARS
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'log'))
#BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OPT_DIR = os.path.join(BASE_DIR, 'opt')

def list_of_functions_per_module(path=OPT_DIR, log=True):
    # search entire file tree for "setup.hpp" files. If found append the module name to the log file
    functions = defaultdict(list)
    for root, dirs, files in os.walk(path):
        for name in files:
            if(name.startswith('fnc_')):
                # after split module is an array of two elements, the actual module name is in the second entry
                module = os.path.split(root)
                module = os.path.split(module[0])
                module = module[1]
                name = os.path.splitext(name)[0][len('fnc_'):]
                functions[module].append(name)

    if log:
        with open(os.path.join(LOG_DIR, "existingFunctions.log"), 'w+') as f:
            for module in functions.keys():
                f.write(module + '\n')
                for fnc in functions[module]:
                    f.write('  ' + fnc + '\n')

    return functions

def list_of_modules(path=OPT_DIR, log=True):
    # search entire file tree for "setup.hpp" files. If found append the module name to the log file
    _modules = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name == "setup.hpp":
                # after split module is an array of two elements, the actual module name is in the second entry
                module = os.path.split(root)
                module = module[1]
                _modules.append(module)
    _modules = sorted(_modules)

    if log:
        with open(os.path.join(LOG_DIR, "existingModules.log"), 'w+') as f:
            for module in _modules:
                f.write(module + '\n')

    return _modules

if __name__ == '__main__':
    # go up one level in file hierarchy, assuming that the folder of this script is in the same directory as the "opt" folder
    # From the base path go into "opt" directory
    if not os.path.isdir(OPT_DIR):
        print("Please make sure that the opt directory is a child directory of the current parent directory. %s was not found." % OPT_DIR)

    # create log folder
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)

    modules = list_of_modules(OPT_DIR)
    for mod in modules:
        print(mod)
    functions = list_of_functions_per_module(OPT_DIR)
    for module, fnc in functions.items():
        print(module, fnc)
    #searchInFiles("EFUNC", optPath)
    #print(find("FEATURES.md", optPath))

