from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:test@localhost:8889/blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'safds3SDFSD'

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,owner):
        self.title = title
        self.owner = owner
    
    def __repr__(self):
        return '<Blog %r>' % self.title

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Blog', backref='owner')

    def __init__(self,name,password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/', methods=['POST', 'GET'])
def index():
    return '<h1>test</h1>'



if __name__ == "__main__":
    app.run()
