from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from . import db
from .models import User, ToDo
from .forms import RegistrationForm, LoginForm, ToDoForm
from . import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Logged in successfully.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ToDoForm()
    if form.validate_on_submit():
        todo = ToDo(task=form.task.data, author=current_user)
        db.session.add(todo)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('dashboard'))
    todos = ToDo.query.filter_by(author=current_user).all()
    return render_template('dashboard.html', title='Dashboard', form=form, todos=todos)

@app.route('/complete/<int:todo_id>')
@login_required
def complete_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    if todo.author != current_user:
        flash('You do not have permission to modify this task.', 'danger')
        return redirect(url_for('dashboard'))
    todo.completed = not todo.completed
    db.session.commit()
    flash('Task status updated.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    if todo.author != current_user:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('dashboard'))
    db.session.delete(todo)
    db.session.commit()
    flash('Task deleted.', 'success')
    return redirect(url_for('dashboard'))
