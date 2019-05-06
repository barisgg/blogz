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

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
    
    def __repr__(self):
        return '%r' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Blog', backref='owner')

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<%r>' % self.name

@app.route('/', methods=['POST', 'GET'])
def index():
    posts = Blog.query.filter_by().all()
    return render_template('home.html', title='Pothole Funhouse', posts=posts)

@app.route('/blog', methods=['GET'])
def blog():
    id = request.args['id']
    post = Blog.query.filter_by(id=id).first()
    return render_template('blog.html', post=post)

    
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=username).first()
        if user and user.password == password:
            session['user'] = username
            flash('logged in')
            redirect('/register')
        else:
            flash('invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password']

        existing_user = User.query.filter_by(name=username).first()

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            redirect('/')

    else:
        flash('invalid username or password', 'error')


    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['user']
    flash('logged out')
    return render_template('login.html')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        owner = User.query.filter_by(name=session['user']).first()
        new_post = request.form['post']
        title = request.form['title']
        submit = Blog(title, new_post, owner)
        db.session.add(submit)
        db.session.commit()
        post = Blog.query.filter_by(title=title).first()
        flash('Post sumbitted')
        return redirect('/blog?id=' + str(post.id))
    
    return render_template('newpost.html')


if __name__ == "__main__":
    app.run()

