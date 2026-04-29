from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm
from app import db
from app.models import User

main = Blueprint('main', __name__)


UNITS = [
    {'code': 'CITS3403', 'name': 'Agile Web Development', 'faculty': 'Engineering & Computing', 'overall': 4.7, 'workload': 3.8, 'reviews': 24},
    {'code': 'CITS1401', 'name': 'Computational Thinking with Python', 'faculty': 'Engineering & Computing', 'overall': 4.5, 'workload': 3.2, 'reviews': 45},
    {'code': 'CITS2002', 'name': 'Systems Programming', 'faculty': 'Engineering & Computing', 'overall': 3.9, 'workload': 2.8, 'reviews': 31},
    {'code': 'PSYC1101', 'name': 'Introduction to Psychology', 'faculty': 'Science', 'overall': 4.3, 'workload': 3.5, 'reviews': 62},
    {'code': 'BIOL1130', 'name': 'From Molecules to Ecosystems', 'faculty': 'Science', 'overall': 3.8, 'workload': 3.2, 'reviews': 15},
    {'code': 'ECON1101', 'name': 'Microeconomics: Prices & Markets', 'faculty': 'Business', 'overall': 3.4, 'workload': 4.1, 'reviews': 50},
    {'code': 'LAWS1101', 'name': 'Law in Context', 'faculty': 'Law', 'overall': 4.2, 'workload': 3.5, 'reviews': 19},
    {'code': 'ARTH1101', 'name': 'Art and Visual Culture', 'faculty': 'Arts', 'overall': 4.6, 'workload': 4.2, 'reviews': 8}
]

@main.route('/')
def index():
    # return '<h1>UWA UniReview - server is running</h1>'
    return render_template('dashboard.html', title='Browse Units')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    login_form    = LoginForm()
    register_form = RegisterForm()
    show_register = request.args.get('tab') == 'signup'

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(user.password_hash, login_form.password.data):
            login_user(user)
            flash(f'Logged in as {user.email}', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html',
                           title='Log in',
                           login_form=login_form,
                           register_form=register_form,
                           show_register=show_register)

@main.route('/register', methods=['POST'])
def register():
    login_form    = LoginForm()
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        existing_user = User.query.filter(
            (User.email == register_form.email.data) | 
            (User.username == register_form.name.data)
        ).first()
        if existing_user:
            flash('Email or username already exists. Please choose a different one.', 'danger')
            return render_template('login.html',
                                   title='Sign up',
                                   login_form=login_form,
                                   register_form=register_form,
                                   show_register=True)
        user = User(
            username=register_form.name.data,
            email=register_form.email.data,
            password_hash=generate_password_hash(register_form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Account created! Welcome to UniReview.', 'success')
        return redirect(url_for('main.index'))

    return render_template('login.html',
                           title='Sign up',
                           login_form=login_form,
                           register_form=register_form,
                           show_register=True)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/api/search')
def search():
    q = request.args.get('q', '').strip().lower()
    faculty = request.args.get('faculty', 'all').strip().lower()

    results = UNITS
    if q:
        results = [u for u in results if q in u['code'].lower() or q in u['name'].lower()]
    if faculty != 'all':
        results = [u for u in results if u['faculty'].lower() == faculty]   

    results = sorted(results, key=lambda u: u['overall'], reverse=True)
    return jsonify(results)
