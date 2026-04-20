from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.forms import LoginForm, RegisterForm

main = Blueprint('main', __name__)


UNITS = [
    {'code': 'CITS3403', 'name': 'Agile Web Development', 'faculty': 'engineering', 'overall': 4.7, 'workload': 3.8, 'reviews': 24},
    {'code': 'CITS1401', 'name': 'Computational Thinking with Python', 'faculty': 'engineering', 'overall': 4.5, 'workload': 3.2, 'reviews': 45},
    {'code': 'CITS2002', 'name': 'Systems Programming', 'faculty': 'engineering', 'overall': 3.9, 'workload': 2.8, 'reviews': 31},
    {'code': 'PSYC1101', 'name': 'Introduction to Psychology', 'faculty': 'science', 'overall': 4.3, 'workload': 3.5, 'reviews': 62},
    {'code': 'BIOL1130', 'name': 'From Molecules to Ecosystems', 'faculty': 'science', 'overall': 3.8, 'workload': 3.2, 'reviews': 15},
    {'code': 'ECON1101', 'name': 'Microeconomics: Prices & Markets', 'faculty': 'business', 'overall': 3.4, 'workload': 4.1, 'reviews': 50},
    {'code': 'LAWS1101', 'name': 'Law in Context', 'faculty': 'law', 'overall': 4.2, 'workload': 3.5, 'reviews': 19},
    {'code': 'ARTH1101', 'name': 'Art and Visual Culture', 'faculty': 'arts', 'overall': 4.6, 'workload': 4.2, 'reviews': 8}
]

@main.route('/')
def index():
    return '<h1>UWA UniReview - server is running</h1>'

@main.route('/login', methods=['GET', 'POST'])
def login():
    login_form    = LoginForm()
    register_form = RegisterForm()
    show_register = request.args.get('tab') == 'signup'

    if login_form.validate_on_submit():
        flash(f'Login attempted for {login_form.email.data}. Database not yet connected.', 'info')
        return redirect(url_for('main.index'))

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
        flash(f'Account created for {register_form.email.data}. Database not yet connected.', 'info')
        return redirect(url_for('main.index'))

    return render_template('login.html',
                           title='Sign up',
                           login_form=login_form,
                           register_form=register_form,
                           show_register=True)
