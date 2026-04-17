from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.forms import LoginForm, RegisterForm

# All routes live in the 'main' blueprint
main = Blueprint('main', __name__)

# ─── Hardcoded unit data ───────────────────────────────────────────────────────
# Temporary data used until the database is set up in Sprint 2.
# Replace with SQLAlchemy queries once models are wired up.
UNITS = [
    { 'code': 'CITS3403', 'name': 'Agile Web Development',             'faculty': 'engineering', 'overall': 4.7, 'workload': 3.8, 'reviews': 24 },
    { 'code': 'CITS1401', 'name': 'Computational Thinking with Python', 'faculty': 'engineering', 'overall': 4.5, 'workload': 4.1, 'reviews': 61 },
    { 'code': 'CITS2002', 'name': 'Systems Programming',               'faculty': 'engineering', 'overall': 3.9, 'workload': 2.8, 'reviews': 43 },
    { 'code': 'CITS3001', 'name': 'Algorithms, Agents and AI',         'faculty': 'engineering', 'overall': 4.2, 'workload': 3.4, 'reviews': 29 },
    { 'code': 'CITS3200', 'name': 'Professional Computing',            'faculty': 'engineering', 'overall': 3.6, 'workload': 3.9, 'reviews': 37 },
    { 'code': 'PSYC1101', 'name': 'Introduction to Psychology',        'faculty': 'science',     'overall': 4.3, 'workload': 3.5, 'reviews': 47 },
    { 'code': 'BIOL1130', 'name': 'From Molecules to Ecosystems',      'faculty': 'science',     'overall': 3.8, 'workload': 3.2, 'reviews': 55 },
    { 'code': 'MATH1011', 'name': 'Multivariable Calculus',            'faculty': 'science',     'overall': 4.2, 'workload': 3.6, 'reviews': 38 },
    { 'code': 'ECON1101', 'name': 'Microeconomics: Prices & Markets',  'faculty': 'business',    'overall': 3.4, 'workload': 2.9, 'reviews': 38 },
    { 'code': 'MGMT2207', 'name': 'Managing People and Organisations', 'faculty': 'business',    'overall': 4.0, 'workload': 3.7, 'reviews': 22 },
    { 'code': 'LAWS1101', 'name': 'Law in Context',                    'faculty': 'law',         'overall': 4.2, 'workload': 3.5, 'reviews': 19 },
    { 'code': 'ARTH1101', 'name': 'Art and Visual Culture',            'faculty': 'arts',        'overall': 4.6, 'workload': 4.2, 'reviews': 31 },
    { 'code': 'HIST2210', 'name': 'Modern Australia',                  'faculty': 'arts',        'overall': 4.1, 'workload': 3.9, 'reviews': 16 },
]


# ─── Page routes ──────────────────────────────────────────────────────────────

@main.route('/')
def index():
    """Dashboard — unit browse page."""
    return render_template('dashboard.html', title='Browse Units')


@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page.
    GET  — render the login/register form.
    POST — validate the login form and flash result.
    Note: actual credential checking against the database comes in Sprint 2.
    """
    login_form    = LoginForm()
    register_form = RegisterForm()

    if login_form.validate_on_submit():
        # Placeholder — replace with database lookup in Sprint 2
        flash(f'Login attempted for {login_form.email.data}. Database not yet connected.', 'info')
        return redirect(url_for('main.index'))

    return render_template('login.html',
                           title='Log in',
                           login_form=login_form,
                           register_form=register_form)


@main.route('/register', methods=['POST'])
def register():
    """
    Handle registration form submission.
    Note: actual user creation in the database comes in Sprint 2.
    """
    register_form = RegisterForm()
    login_form    = LoginForm()

    if register_form.validate_on_submit():
        # Placeholder — replace with db.session.add(user) in Sprint 2
        flash(f'Account created for {register_form.email.data}. Database not yet connected.', 'info')
        return redirect(url_for('main.index'))

    # If validation failed, re-render login page showing register form with errors
    return render_template('login.html',
                           title='Sign up',
                           login_form=login_form,
                           register_form=register_form,
                           show_register=True)


# ─── AJAX API routes ──────────────────────────────────────────────────────────

@main.route('/api/search')
def api_search():
    """
    AJAX endpoint for live unit search on the dashboard.

    Query parameters:
        q       - search string (matches unit code or name)
        faculty - faculty filter (e.g. 'engineering', 'science', 'all')

    Returns JSON array of matching units, sorted by overall rating descending.

    Example:
        GET /api/search?q=cits&faculty=all
        GET /api/search?q=&faculty=science
    """
    q       = request.args.get('q', '').lower().strip()
    faculty = request.args.get('faculty', 'all').lower().strip()

    results = []
    for unit in UNITS:
        # Apply faculty filter
        if faculty != 'all' and unit['faculty'] != faculty:
            continue
        # Apply search filter — match on code or name
        if q and q not in unit['code'].lower() and q not in unit['name'].lower():
            continue
        results.append(unit)

    # Sort by overall rating descending
    results.sort(key=lambda u: u['overall'], reverse=True)

    return jsonify(results)
