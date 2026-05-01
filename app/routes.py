from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm
from app import db
from app.models import User, Unit, Review

main = Blueprint('main', __name__)

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
    q       = request.args.get('q', '').strip()
    faculty = request.args.get('faculty', '').strip()

    query = Unit.query

    if q:
        query = query.filter(
            db.or_(
                Unit.name.ilike(f'%{q}%'),
                Unit.code.ilike(f'%{q}%')
            )
        )

    if faculty and faculty != 'all':
        query = query.filter_by(faculty=faculty)

    units = query.all()
    return jsonify([u.to_dict() for u in units])

@main.route('/unit/<code>')
def unit_detail(code):
    unit    = Unit.query.filter_by(code=code).first_or_404()
    reviews = Review.query.filter_by(unit_id=unit.id).all()
    return render_template('unit.html', unit=unit, reviews=reviews)