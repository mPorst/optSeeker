import os
import re

# Script for walking through the OPT mission and searching for function calls
# to check where which functions are called
#
# Author: MAPster
#
# 
#
#

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

def findFunctions(path):
    # delete any previously generated logs by opening in truncate mode (w) or create if not already created (+)
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(scriptPath, "existingFunctions.log"), 'w+')
    f.close
    # open file in append mode
    f = open(os.path.join(scriptPath, "existingFunctions.log"), 'a')
    # search entire file tree for "setup.hpp" files. If found append the module name to the log file 
    functions = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if("fnc_" in name):
                # after split module is an array of two elements, the actual module name is in the second entry
                module = os.path.split(root)
                module = os.path.split(module[0])
                module = module[1]
                name = name.split('fnc_')
                name = name[1].split('.sqf')
                name = name[0]
                print(module + " has function " + name)
                f.write(module + "-" + name + "\n")
                #print(module)
                #print(os.path.join(root, name))

def findModules(path):
    # delete any previously generated logs by opening in truncate mode (w) or create if not already created (+)
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(scriptPath, "existingModules.log"), 'w+')
    f.close
    # open file in append mode
    f = open(os.path.join(scriptPath, "existingModules.log"), 'a')
    # search entire file tree for "setup.hpp" files. If found append the module name to the log file 
    modules = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if(name == "setup.hpp"):
                # after split module is an array of two elements, the actual module name is in the second entry
                module = os.path.split(root)
                module = module[1]
                f.write(module + "\n")
                modules.append(module)
                #print(module)
                #print(os.path.join(root, name))
    return modules

#call this function ONLY after findModules and findFunctions


# get current path of the python file
path = os.path.dirname(os.path.abspath(__file__))
# go up one level in file hierarchy, assuming that the folder of this script is in the same directory as the "opt" folder
newPath = os.path.split(path)
basePath = newPath[0] # the first element of newPath holds the base path, the second the directory
# From the base path go into "opt" directory
optPath = os.path.join(basePath, "opt")
modules = findModules(optPath)
for mod in modules:
    print(mod)
findFunctions(optPath)
#searchInFiles("EFUNC", optPath)
#print(find("FEATURES.md", optPath))
