from flask import render_template
from .import views

@views.route('/')
def index():
    return render_template('base.html')

@views.route('/display/<int:id>')
def display(id):
    return render_template('display.html')