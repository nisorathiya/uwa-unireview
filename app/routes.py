from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm, ReviewForm
from app import db
from app.models import User, Unit, Review, Vote

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
    """Fetch unit by code and render the unit detail page."""
    unit = Unit.query.filter_by(code=code).first_or_404()

    reviews_raw  = Review.query.filter_by(unit_id=unit.id)\
                               .order_by(Review.created_at.desc()).all()
    review_count = len(reviews_raw)

    if review_count > 0:
        avg_overall    = round(sum(r.overall_rating    for r in reviews_raw) / review_count, 1)
        avg_workload   = round(sum(r.workload_rating   for r in reviews_raw) / review_count, 1)
        avg_difficulty = round(sum(r.difficulty_rating for r in reviews_raw) / review_count, 1)
        avg_usefulness = round(sum(r.usefulness_rating for r in reviews_raw) / review_count, 1)
    else:
        avg_overall = avg_workload = avg_difficulty = avg_usefulness = 0

    # attach vote info to each review (zeros for now until vote route exists)
    for r in reviews_raw:
        r.upvotes   = 0
        r.downvotes = 0
        r.user_vote = None

    user_has_reviewed = False
    is_saved = False
    if current_user.is_authenticated:
        user_has_reviewed = Review.query.filter_by(
            unit_id=unit.id, user_id=current_user.id
        ).first() is not None

    similar_units = Unit.query.filter(
        Unit.faculty == unit.faculty, Unit.id != unit.id
    ).limit(4).all()

    form = ReviewForm()

    return render_template('unit.html',
                           unit=unit,
                           reviews=reviews_raw,
                           review_count=review_count,
                           avg_overall=avg_overall,
                           avg_workload=avg_workload,
                           avg_difficulty=avg_difficulty,
                           avg_usefulness=avg_usefulness,
                           user_has_reviewed=user_has_reviewed,
                           is_saved=is_saved,
                           similar_units=similar_units,
                           form=form)

# Submit a review
@main.route('/review/submit', methods=['POST'])
@login_required
def submit_review():
    form = ReviewForm()
    unit_code = request.form.get('unit_code')
    unit = Unit.query.filter_by(code=unit_code).first_or_404()

    # Enforce one review per student per unit
    existing = Review.query.filter_by(
        unit_id=unit.id, user_id=current_user.id
    ).first()
    if existing:
        flash('You have already reviewed this unit.', 'warning')
        return redirect(url_for('main.unit_detail', code=unit.code))

    if form.validate_on_submit():
        review = Review(
            user_id           = current_user.id,
            unit_id           = unit.id,
            overall_rating    = form.overall_rating.data,
            workload_rating   = form.workload_rating.data,
            difficulty_rating = form.difficulty_rating.data,
            usefulness_rating = form.usefulness_rating.data,
            comment           = form.comment.data,
            year_taken        = int(request.form.get('year_taken', 2024)),
            semester          = request.form.get('semester', 'S1')
        )
        db.session.add(review)
        db.session.commit()
        flash('Your review has been posted!', 'success')
    else:
        flash('Please fix the errors in your review.', 'danger')

    return redirect(url_for('main.unit_detail', code=unit.code))


# Edit a review
@main.route('/review/edit/<int:review_id>', methods=['POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)

    # Only the owner can edit
    if review.user_id != current_user.id:
        flash('You can only edit your own reviews.', 'danger')
        return redirect(url_for('main.unit_detail', code=review.unit.code))

    form = ReviewForm()
    if form.validate_on_submit():
        review.overall_rating    = form.overall_rating.data
        review.workload_rating   = form.workload_rating.data
        review.difficulty_rating = form.difficulty_rating.data
        review.usefulness_rating = form.usefulness_rating.data
        review.comment           = form.comment.data
        db.session.commit()
        flash('Your review has been updated.', 'success')
    else:
        flash('Please fix the errors in your review.', 'danger')

    return redirect(url_for('main.unit_detail', code=review.unit.code))


# Delete a review
@main.route('/review/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    # Only the owner can delete
    if review.user_id != current_user.id:
        flash('You can only delete your own reviews.', 'danger')
        return redirect(url_for('main.unit_detail', code=review.unit.code))

    unit_code = review.unit.code
    # Delete associated votes first
    Vote.query.filter_by(review_id=review_id).delete()
    db.session.delete(review)
    db.session.commit()
    flash('Your review has been deleted.', 'info')
    return redirect(url_for('main.unit_detail', code=unit_code))