from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

todos = []  # A simple in-memory task list

@main.route('/')
def index():
    return render_template('index.html', todos=todos)

@main.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    todos.append(task)
    return redirect(url_for('main.index'))

@main.route('/delete/<int:task_id>')
def delete(task_id):
    todos.pop(task_id)
    return redirect(url_for('main.index'))
