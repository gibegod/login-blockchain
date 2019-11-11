from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from forms import SignupForm, PostForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/miniblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from models import User, Post


@app.route("/")
def index():
    posts = Post.get_all()
    return render_template("index.html", posts=posts)

@app.route("/account")
def account():
    return render_template("myaccount.html")


@app.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html", post=post)


@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()

        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm(request.form)
    if request.method == 'POST': 
        if form.validate():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user is None:
                # Creamos el usuario y lo guardamos
                user = User(name=name, email=email)
                user.set_password(password)
                user.save()
                # Dejamos al usuario logueado
                login_user(user, remember=True)
                return redirect(url_for('account'))
            flash('A user already exists with that email address.')
            return redirect(url_for('show_signup_form'))
    return render_template("signup_form.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = request.form.get('email')
            password = request.form.get('password')  
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('account'))
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    return render_template('login_form.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
