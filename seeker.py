import os
import re
from collections import defaultdict

# Script for walking through the OPT mission and searching for function calls
# to check where which functions are called
#
# Author: MAPster
#
#
#
#
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'log'))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OPT_DIR = os.path.join(BASE_DIR, 'opt')

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def searchInFiles(expr, path):
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(scriptpath, "functionCalls.log", 'w+'))
    for root, dirs, files in os.walk(path):
        for name in files:
            # for each file split name to check file ending
            splitName = name.split('.')
            fileEnding = splitName[len(splitName)-1]
            # if file ending is one of the following: read file and search for expr
            if(fileEnding == "sqf" or fileEnding == "hpp"):
                #print("Now opening " + name)
                f = open(os.path.join(root,name), "r")
                line = "This is just a helper string because line needs to be defined for the while loop and python does not support do-while loops..."
                while(line != ''):
                    line = f.readline()
                    if expr in line:
                        print("found " + expr + " in file " + name + "\n" + line)

def findFunctions(path, log=True):
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
    

def findModules(path, log=True):
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


#call this function ONLY after findModules and findFunctions

# go up one level in file hierarchy, assuming that the folder of this script is in the same directory as the "opt" folder
# From the base path go into "opt" directory
if not os.path.isdir(OPT_DIR):
    print("Please make sure that the opt directory is a child directory of the current parent directory. %s was not found." % optPath)

# create log folder
if not os.path.isdir(LOG_DIR):
    os.mkdir("log")

modules = findModules(OPT_DIR)
for mod in modules:
    print(mod)
functions = findFunctions(OPT_DIR)
for module, fnc in functions.items():
    print(module, fnc)
#searchInFiles("EFUNC", optPath)
#print(find("FEATURES.md", optPath))
