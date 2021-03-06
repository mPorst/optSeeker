import os
from collections import defaultdict


# GLOBAL VARS
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'log'))
#BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OPT_DIR = os.path.join(BASE_DIR, 'opt')
END_HEADER = '#include "script_component.hpp"'
HEADER_KEYS = ['Description:', 'Author:', 'Arguments:', 'Return Value:', 'Server only:', 'Public:', 'Global:', 'Sideeffects:', 'Example:']


def list_of_functions_per_module(return_attributes, path=OPT_DIR, log=False):
    # search entire file tree for "setup.hpp" files. If found append the module name to the log file
    all_functions = defaultdict(list)
    all_attributes = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.startswith('fnc_'):
                # after split module is an array of two elements, the actual module name is in the second entry
                module = os.path.split(root)
                module = os.path.split(module[0])
                module = module[1]
                name = os.path.splitext(name)[0][len('fnc_'):]
                result_dict = read_fnc(module, name, return_attributes)
                all_functions[module].append(name)
                all_attributes[(module, name)] = result_dict['attributes']

    if log:
        with open(os.path.join(LOG_DIR, "existingFunctions.log"), 'w+') as f:
            for module in all_functions.keys():
                f.write(module + '\n')
                for fnc in all_functions[module]:
                    f.write('  ' + fnc + '\n')

    return {'functions': all_functions, 'attributes': all_attributes}


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


def read_fnc(module, fnc, return_attributes=True):
    """find function in module/functions folder and read out its header as key => value pairs"""
    header = defaultdict(list)
    fnc_name_full = 'fnc_{0}.sqf'.format(fnc)
    result = {}
    
    # find correct folder
    for root, dirs, files in os.walk(OPT_DIR):
        if fnc_name_full in files:
            if os.path.basename(os.path.split(root)[0]) == module:
                # read in whole content
                with open(os.path.join(root, fnc_name_full)) as fhandle:
                    content = fhandle.read()

                # if header can be found
                if content.find(END_HEADER) != -1:
                    header_raw, content = content.split(END_HEADER)

                    # transform raw header into separate lines
                    header_split = [x for x in header_raw.split('\n') if x.strip() not in ['/**', '*', '*/', '']]

                    # read in the content of one key until empty line
                    last_seen_key = ''
                    key_found = False
                    for line in header_split:
                        for key in HEADER_KEYS:
                            if line.find(key) != -1:
                                last_seen_key = key
                                key_found = True
                                break

                        # if there was a new key, jump to next line
                        if key_found:
                            key_found = False
                            continue
                        
                        if last_seen_key != '':
                            header[last_seen_key[:-1]].append(line.strip('*').strip())
                break
    
    result['header'] = header
    result['content'] = content
    
    if return_attributes:
        result['attributes'] = process_fnc_header(header)

    return result


def process_fnc_header(header):
    result = {}
    if "Public" in header:
        if any([True for line in header['Public'] if line.startswith('yes')]):
            result['Public'] = True
    if "Global" in header:
        if any([True for line in header['Global'] if line.startswith('yes')]):
            result['Global'] = True
    if "Server only" in header:
        if any([True for line in header['Server only'] if line.startswith('yes')]):
            result['Server only'] = True
    if "Sideeffects" in header:
        if header['Sideeffects']:
            result['Sideeffects'] = True
            
    return result


# create log folder
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)


if __name__ == '__main__':
    # go up one level in file hierarchy, assuming that the folder of this script is in the same directory as the "opt" folder
    # From the base path go into "opt" directory
    if not os.path.isdir(OPT_DIR):
        print("Please make sure that the opt directory is a child directory of the current parent directory. %s was not found." % OPT_DIR)

    #modules = list_of_modules(OPT_DIR)
    #for mod in modules:
        #print(mod)
    functions, attributes = list_of_functions_per_module(OPT_DIR, log=False)
    #for module, fnc in functions.items():
        #print(module, fnc)

    #header, content, attributes = read_fnc('beam', 'beam')
    #searchInFiles("EFUNC", optPath)
    #print(find("FEATURES.md", optPath))

