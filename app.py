from flask import Flask, url_for, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import RETAIN_SCHEMA
from flask_wtf import FlaskForm, form
from wtforms import StringField, SubmitField


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passone@35.242.140.217:3306/todo_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config["SECRET_KEY"] = 'hufhhdj'

db = SQLAlchemy(app)

class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50), nullable = False)
    complete = db.Column(db.Boolean, default=False)


class TodoForm(FlaskForm):
    task = StringField("Task")
    submit =  SubmitField("Add Todo")
    delete = SubmitField("Delete")

@app.route('/')
def home():
    form=TodoForm()
    return render_template("home.html", form=form)
    

@app.route('/index', methods=["GET", "POST"])
def index():

    todo_list = TodoList()
    alltasks = todo_list.query.all()
    form = TodoForm()

    return render_template("index.html", alltasks=alltasks, todo_list=todo_list, form=form)



@app.route('/complete/<int:todo_id>')
def complete(todo_id): 
    completeme = TodoList.query.get(todo_id)
    completeme.complete = True
    db.session.commit()
    return redirect(url_for("/index"))

# url_for("complete", todo_id=4)

@app.route('/incomplete/<int:todo_id>')
def incomplete(todo_id): 
    completeme = TodoList.query.get(todo_id)
    completeme.complete = False
    db.session.commit()
    return redirect(url_for("/index"))

@app.route('/add', methods = ["GET", "POST"])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = TodoList(task=form.task.data)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html", form=form)


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = TodoList.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>', methods = ["GET", "POST"])
def update(todo_id):
    # form=TodoForm()
    # return render_template("update.html", form=form)

    form = TodoForm()
    todo_update = TodoList.query.get(todo_id)

    if form.validate_on_submit():
        todo_update.task = form.task.data
        db.session.commit()
        return redirect(url_for("index"))
    elif request.method == "GET":
        form.task.data = todo_update.task

    return render_template("update.html", form=form)


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')