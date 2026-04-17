from flask import Blueprint, render_template, request, jsonify

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
    return render_template('dashboard.html', title='Browse Units')

@main.route('/login')
def login():
    return render_template('login.html', title='Log in') 

@main.route('/api/search')
def api_search():
    q = request.args.get('q', '').lower().strip() 
    faculty = request.args.get('faculty', 'all').lower().strip()
    
    results = []
    for unit in UNITS:
        if faculty != 'all' and unit['faculty'] != faculty:
            continue
        if q and q not in unit['code'].lower() and q not in unit['name'].lower():
            continue
        results.append(unit)
    
    results.sort(key=lambda u: u['overall'], reverse=True)
    return jsonify(results)