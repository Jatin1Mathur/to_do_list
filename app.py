from flask import Flask, render_template, request, redirect, url_for, flash
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasetodos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class StatusEnum(Enum):
    PENDING = 0
    COMPLETED = 1

class databaseTodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255), nullable=True)
    checked = db.Column(db.Enum(StatusEnum), default=StatusEnum.PENDING)

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        todo_name = request.form["todo_name"]
        description = request.form.get("description", "")
        if not todo_name:
            flash("Enter your task", "error")
        else:
            new_todo = databaseTodo(name=todo_name, description=description)
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for("home"))
    todos = databaseTodo.query.all()
    return render_template("index.html", items=todos)

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    todo = databaseTodo.query.get_or_404(todo_id)
    todo.checked = (StatusEnum.COMPLETED if todo.checked == StatusEnum.PENDING else StatusEnum.PENDING)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    todo = databaseTodo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)





