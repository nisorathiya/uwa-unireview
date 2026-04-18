from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm

main = Blueprint('main', __name__)

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