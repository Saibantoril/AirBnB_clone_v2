#!/usr/bin/python3
"""
This module defines a Flask web application with several routes.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Displays "Hello HBNB!".
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays "HBNB".
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Takes a variable from the URL and displays a message with "C"
    followed by the value of the variable.
    """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """
    Takes a variable from the URL and displays a message with "Python"
    followed by the value of the variable.
    """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Takes an integer from the URL and displays a message indicating that
    it is a number.
    """
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Takes an integer from the URL and renders an HTML template with the
    value of the integer in an H1 tag.
    """
    return render_template('number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Takes an integer from the URL and renders an HTML template indicating
    whether it is odd or even.
    """
    return render_template('number_odd_or_even.html', number=n, parity='even' if n % 2 == 0 else 'odd')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

