from flask import Blueprint, render_template, request
from app.forms import LoginForm, RegisterForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return '<h1>UWA UniReview- server is running</h1>'

@main.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    show_register = request.args.get('tab') == 'signup'
    return render_template('login.html',
                           title='Log in',
                           login_form=login_form,
                           register_form=register_form,
                           show_register=show_register)

@main.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template('login.html',
                           title='Create account',
                           login_form=login_form,
                           register_form=register_form,
                           show_register=True) 