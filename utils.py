

from flask import Flask, render_template, request, redirect, url_for, flash , get_flashed_messages
from model.models import db,databaseTodo,StatusEnum


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasetodos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'secret_key'
    db.init_app(app)
    return app

def register_routes(app):
    def home():
        todos = databaseTodo.query.all()
        messages = get_flashed_messages(with_cotegories = True)
        return render_template('index.html' , todos = todos, messages = messages)
    
            
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

    @app.route("/checked/<int:todo_id>", methods=["POST", "PUT"])
    def checked_todo(todo_id):
        todo = databaseTodo.query.get_or_404(todo_id)
        if request.method == "PUT":
            todo.checked = StatusEnum.COMPLETED
        elif request.method == "PATCH":
            todo.checked = StatusEnum.PENDING if todo.checked == StatusEnum.COMPLETED else StatusEnum.COMPLETED
        db.session.commit()
        flash('Task "{}" status updated.'.format(todo.name), 'success')
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
    app = create_app()
    register_routes(app)
    app.run(debug=True)
        
