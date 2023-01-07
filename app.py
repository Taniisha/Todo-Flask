#flask is a python module that provides us functionality to create web apps
from flask import Flask, render_template, request, redirect  #importing flask from flask package
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)    #initializing app

#SQL alchemy is an ORM mapper that facilitates us to make changes in database trough Python
#for this we need to install flask-sqlalchemy package

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" #initializing sqlalchemy with the database URI that should be used for connection

#creating the SQLAlchemy object by passing it the flask application.
#This object contains all the functions and helpers from both sqlalchemy and sqlalchemy.orm. Furthermore it provides a class called Model that is a declarative base which can be used to declare models
db= SQLAlchemy(app) #Integrates SQLAlchemy with Flask. This handles setting up one or more engines, associating tables and models with specific engines, and cleaning up connections and sessions after each request.


#for creating a database, we need to make a database class
class Todo(db.Model):    #after creating this class, in python terminal-> from app import db   db.create_all()  -> this  will create todo.db file and _pycache_ in our  directory, hence by this command we are creating database and tables
    __tablename__ = "Todo"
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String,nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:       #this function states that what do you want to return when u call Todo class object, it is like stringer method in golang
        return f"{self.sno}-{self.title}"

class Done(db.Model):
    __tablename__ = "Done"
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String,nullable=True)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
    

@app.route('/', methods=["GET","POST"])     #declaring end points
def add_todo():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, desc=desc)  #creating instance
        db.session.add(todo)  #to add in database
        db.session.commit()  #commit the changes to db
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)       #to render templates, the attributes would be available to index.html

@app.route('/done/<int:sno>')
def todo_done(sno):
    todo = Todo.query.filter_by(sno=sno).first()    #to fetch the first record that match the filter from db
    db.session.delete(todo)
    db.session.commit()
    done_todo = Done(title=todo.title, desc=todo.desc)  #creating instance
    db.session.add(done_todo)  #to add in database
    db.session.commit()  #commit the changes to db
    # render_template("done.html",done=done)       #to render templates, the attributes would be available to index.html
    return redirect("/")

@app.route('/done')
def show_done():
    done = Done.query.all()
    return render_template("done.html",done=done)       #to render templates, the attributes would be available to index.html

@app.route('/delete_done')
def delete_done():
    Done.query.delete()   #to delete all the records in database
    db.session.commit()
    return redirect("/done")


@app.route('/update/<int:sno>',methods=["GET","POST"])
def todo_update(sno):
    todo = Todo.query.filter_by(sno=sno).first()    #to fetch the first record that match the filter from db
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo.title = title
        todo.desc = desc
        db.session.add(todo)  #to add in database
        db.session.commit()  #commit the changes to db
        return redirect("/")
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>')
def todo_delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()    #to fetch the first record that match the filter from db
    db.session.delete(todo)
    db.session.commit()
    return redirect("/") 

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True,port=3000)   #debug=True means to display error on browser itself