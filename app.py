import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import ToDoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class ToDo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/todos', methods=['GET', 'POST'])
def todo_list():
    form = ToDoForm()
    if form.validate_on_submit():
        todo = ToDo(description=form.description.data, status='Undone')
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo_list'))
    todos = ToDo.query.order_by(ToDo.status != 'Completed').all()
    return render_template('todo_list.html', todos=todos, form=form)

@app.route('/todos/add', methods=['GET', 'POST'])
def add_todo():
    form = ToDoForm()
    if form.validate_on_submit():
        todo = ToDo(description=form.description.data, status='Undone')
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo_list'))
    return render_template('add_todo.html', form=form)



@app.route('/todos/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    form = ToDoForm()

    if form.validate_on_submit():
        todo.description = form.description.data
        db.session.commit()
        return redirect(url_for('todo_list'))

    return render_template('edit_todo.html', todo=todo, form=form)

@app.route('/todos/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo_list'))

@app.route('/todos/mark_done/<int:todo_id>', methods=['POST'])
def mark_done(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    
    if todo.status == 'Completed':
        todo.status = 'Undone'
    else:
        todo.status = 'Completed'
    
    db.session.commit()
    return redirect(url_for('todo_list'))


if __name__ == '__main__':
    app.run(debug=True)  

