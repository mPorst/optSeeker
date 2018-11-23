"""
Docstring for this application
"""
from flask import Flask, render_template
from opt_seeker import list_of_functions_per_module, read_fnc

functions_cache = {}
attributes_cache = {}

# FLASK APP initialization
app = Flask(__name__)

@app.before_first_request
def  read_in_functions():
    """
    read in opt directory with all functions and their attributes
    :return:
    functions_cache: dict - list of all functions keyed by their module
    attributes_cache: dict - list of header data keyed by (module,function)
    """
    global functions_cache, attributes_cache
    result_dict = list_of_functions_per_module()
    functions_cache, attributes_cache = result_dict['functions'], result_dict['attributes']
    
# ROUTES
@app.route('/')
@app.route('/functions')
def opt_overview():
    """
    render all modules and their associated functions
    """

    return render_template(
        'page-functions.html',
        title='Functions',
        functions=functions_cache,
        attributes=attributes_cache,
    )

@app.route('/functions/<string:module>/<string:fnc>')
def opt_function_header(module, fnc):
    """
    read in function specified by module and fnc
    :param module: name of the module
    :param fnc: name of the function
    :return:
    """
    return_dict = read_fnc(module, fnc, return_attributes=False)
    fnc_name_full = 'fnc_{0}.sqf'.format(fnc)

    return render_template(
        'page-function-header.html',
        title=fnc_name_full,
        module=module,
        function=fnc,
        functions=functions_cache,
        attributes=attributes_cache,
        header=return_dict['header'],
        content=return_dict['content']
    )


if __name__ == '__main__':
    app.run()

