from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from . import graph
from .. import client,db_name,db_type

@graph.route('/graph', methods=['GET', 'POST'])
def graph():
    return render_template('graph.html')