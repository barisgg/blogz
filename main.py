from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bloz:test@localhost:8889/bloz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'safds3SDFSD'
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    body = db.Column(db.String(2000))
    name = db.relationship('User', backref='user_name')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
    
    def __repr__(self):
        return str(self.owner)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120))
    name = db.Column(db.String(250))
    posts = db.relationship('Blog', backref='owner')

    def __init__(self, user_name, password):
        self.name = user_name
        self.password = password

    def __repr__(self):
        return '<%r>' % self.name

@app.before_request
def require_login():
    username = ''
    allowed = ["/", "login", "register", "logout", "static"]
    if 'user' not in session  and request.endpoint not in allowed:
        return redirect('/login')

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.filter_by().all()
    return render_template('index.html', title="Pothole Funhouse", users=users)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    posts = Blog.query.filter_by().all()
    users = User.query.filter_by().all()
    return render_template('blog.html', title='Pothole Funhouse', posts=posts, users=users)

@app.route('/post', methods=['GET'])
def post():
    id = request.args['id']
    post = Blog.query.filter_by(id=id).first()
    return render_template('post.html', post=post)

    
@app.route('/login', methods=['POST', 'GET'])
def login():
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=username).first()
        if user and user.password == password:
            session['user'] = username
            flash('logged in')
            return redirect('/newpost')
        if not username:
            flash('username left blank')
            if not password:
                flash('password left blank')
            return redirect('login')
        if not user:
            flash('username does not exist', 'error')
            return redirect('/login')
        else:
            if not User.query.filter_by(name=username, password=password).all():
                flash('incorrect password', "error")
                return render_template('login.html', username=username)
    return render_template('login.html', username=username)
    

@app.route('/register', methods=['POST', 'GET'])
def register():
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        existing_user = User.query.filter_by(name=username).first()

        if not existing_user and username and password and password == password2:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            flash('logged in')
            return redirect('/newpost')
        elif password and not password2:
            flash('please repeat password', 'error')
        
        if existing_user:
            flash('username taken', 'error')
            redirect('/register')
 
        if not password or not username and password == password2:
            flash('one or more fields left blank', 'error')
            redirect('/register')
        
       
    return render_template('register.html', username=username)

@app.route('/logout')
def logout():
    del session['user']
    flash('logged out')
    return redirect('/')

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
        return redirect('/post?id=' + str(post.id))
    
    return render_template('newpost.html')


if __name__ == "__main__":
    app.run()

