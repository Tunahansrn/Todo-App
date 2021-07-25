from functools import total_ordering
from logging import debug
from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query, session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/tunah/Desktop/Todo-App/todo.db'
db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    nwtodo = todo.query.all()
    return render_template("index.html",todos = nwtodo)

@app.route("/add",methods=["POST"])
def add():
    title = request.form.get("title")
    if not title:
        return redirect(url_for("index"))
    else:
        newtodo = todo(title=title,complete = False)
        db.session.add(newtodo)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def complete(id):
    nwtodo = todo.query.filter_by(id = id).first()
    nwtodo.complete = not nwtodo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete(id):
    newtodo = todo.query.filter_by(id = id).first()
    db.session.delete(newtodo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)