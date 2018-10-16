"""
Docstring for this application
"""
from flask import Flask, render_template
from opt_seeker import list_of_modules, list_of_functions_per_module, read_fnc

# FLASK APP initialization
app = Flask(__name__)

# ROUTES
@app.route('/')
@app.route('/functions')
def opt_overview():

    modules = list_of_modules()
    functions = list_of_functions_per_module()

    return render_template(
        'page-functions.html',
        title='Functions',
        functions=functions
    )

@app.route('/functions/<string:module>/<string:fnc>')
def opt_function_header(module, fnc):
    header, content = read_fnc(module, fnc)
    functions = list_of_functions_per_module()
    fnc_name_full = 'fnc_{0}.sqf'.format(fnc)
    
    return render_template(
        'page-function-header.html',
        title=fnc_name_full,
        module=module,
        function=fnc,s
        functions=functions,
        header=header,
        content=content
    )


if __name__ == '__main__':
    app.run()

