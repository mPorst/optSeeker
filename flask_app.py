"""
Docstring for this application
"""
from flask import Flask, render_template
from opt_seeker import list_of_modules, list_of_functions_per_module

# FLASK APP initialization
app = Flask(__name__)

# ROUTES
@app.route('/')
def opt_overview():

    modules = list_of_modules()
    functions = list_of_functions_per_module()

    return render_template('index.html', title='OPT Seeker', functions=functions)

