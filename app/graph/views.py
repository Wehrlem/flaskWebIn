from flask import render_template
from . import graph

@graph.route('/graph', methods=['GET', 'POST'])
def graph():
    return render_template('graph.html')