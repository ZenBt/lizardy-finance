from flask import redirect, request, render_template, render_template, request, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app
from models import User
from models import db
from forms import LoginForm, RegForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@login_required
def index():
    return '''Yup
<a href="/logout"> Logout </a>>'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.pwd.data
        print(type(email), type(password))
        try:
            user_info = User.query.filter_by(email = email).first()
            if user_info is None:
                flash('User not found')
                print(1)
            elif user_info.check_password(password):
                print(email, password)
                login_user(user_info)
                return redirect(url_for('index'))
            else:
                print(2)
                flash('Invalid password')
        except:
            print('DB error')
    return render_template('login.html', form=form)
       

@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegForm()
    email = form.email.data
    password = form.pwd.data
    print(email, password)
    if form.validate_on_submit():
        print(1)
        user = User(email=email).set_password(password)
        print(user)
        try:
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            print('DB error')
    return render_template('singup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    