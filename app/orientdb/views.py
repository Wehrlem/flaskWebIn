from flask import render_template
from . import orient


@orient.route('/orientdb')
def graph():
    return render_template('orientdb.html')