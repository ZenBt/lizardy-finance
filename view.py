from flask import redirect, render_template, render_template, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func, desc
from app import app
from models import User, Expenses, Tags
from models import db
from forms import LoginForm, RegForm, AddExpense, AddTag

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    form = AddExpense()
    form.tag.choices = [(tag.id, tag.tag)
                        for tag in Tags.query.filter(Tags.user_id==current_user.id).order_by(Tags.tag)]
    if not form.tag.choices:
        return redirect(url_for('category'))
    
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data or None
        tag = form.tag.data
        cost = form.cost.data
        db.session.add(Expenses(
            name=name,
            description=description,
            cost=cost,
            tag_id=tag,
            user_id=current_user.id))
        db.session.commit()
        return redirect(url_for('index'))
    history = Expenses.query.filter(Expenses.user_id==current_user.id).order_by(Expenses.date_time).all()[:20]
    return render_template('index.html', form=form, history=history)


@app.route('/add-category', methods=['POST', 'GET'])
@login_required
def category():
    form = AddTag()
    tags = Tags.query.with_entities(Tags.tag,
                                     func.count(Tags.tag)).group_by(Tags.tag).order_by(func.count(Tags.tag).desc()).all()
    if form.validate_on_submit():
        name_tag = form.tag.data
        tag = Tags(tag=name_tag, user_id=current_user.id)
        try:
            db.session.add(tag)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print('DB error')
        return redirect(url_for('category'))
    return render_template('category.html', form=form, tags=tags)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.pwd.data
        try:
            user_info = User.query.filter_by(email = email).first()
            if user_info is None:
                flash('User not found')
            elif user_info.check_password(password):
                login_user(user_info)
                return redirect(url_for('index'))
            else:
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
    if form.validate_on_submit():
        user = User(email=email).set_password(password)
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
    
