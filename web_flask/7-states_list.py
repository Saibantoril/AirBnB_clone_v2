#!/usr/bin/python3

"""
This module starts a Flask web application to display a list of states from a storage engine.
"""


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Renders an HTML page that displays a list of all states sorted by name.

    Returns:
        A string with the HTML content of the page.
    """
    states = storage.all()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the SQLAlchemy session after each request.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
