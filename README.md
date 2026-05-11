# UWA UniReview

A student-driven web application where UWA students can see and share honest reviews of units before enrolling. Browse units across all faculties, read peer reviews of workload, difficulty and usefulness, save units for later, vote on helpful reviews, and contribute your own experiences to help fellow students make informed choices.

---

## Team

| UWA ID | Full Name | GitHub Username | Role |
|----------|------------|-----------------|---------------------|
| 24667496 | Nidhi Sorathiya | [@nisorathiya](https://github.com/nisorathiya) | Project Lead / Documentation / Full-stack developer |
| 24500079 | Nevis Herlangga | [@nxherl](https://github.com/nxherl) | Documentation & Wireframing / Full-stack developer |
| 24726135 | Md Mahabub Islam | [@ProgMahabub21](https://github.com/ProgMahabub21) | Full-stack developer |
| 25167515 | Xingyan Guo | [@laomeile](https://github.com/laomeile) | Full-stack developer |

---

## Purpose and Design

UniReview helps UWA students discover what they are actually signing up for when choosing units. Course handbooks describe the syllabus, but they don't tell you whether the workload is reasonable, whether the lecturer is engaging, or whether the assessment/group project is fair. UniReview fills that gap- students review units they already completed and future students benefit from the collective knowledge.

**Key design principles:**
- **Honest** — reviews are written by verified UWA students using their `@student.uwa.edu.au` email
- **Structured** — every review captures four dimensions (overall, workload, difficulty, usefulness) on a 1–5 scale
- **Discoverable** — fast unit search with live filtering by faculty
- **Community-driven** — users vote helpful reviews up, building a credibility signal

---

## Features

**Authentication and accounts**
- Register with a UWA student email (validated)
- Secure password hashing using werkzeug
- Login / logout with session management via flask-login
- CSRF protection on all forms

**Browsing units**
- Dashboard with 32+ seeded UWA units across 5 faculties
- Live AJAX search by unit code or name
- Faculty filter pills (Engineering & Computing, Science, Business, Law, Arts)
- Aggregated rating displayed on each unit card
- Dynamic site-wide stats (total units, total reviews, average score)

**Unit detail page**
- Hero section with unit info, average overall rating, and save button
- Stats bar showing average across 4 dimensions with progress bars
- Full list of reviews with vote counts and clickable author profiles
- **Rating distribution chart** using Chart.js can help see how reviews are spread across 1–5 stars
- Sidebar with unit info and similar units

**Reviews**
- Submit a review with rating sliders and a written comment (min 20 chars)
- One review per user per unit (enforced both client and server-side)
- Edit or delete your own reviews
- Upvote/downvote helpful reviews via AJAX (toggle behaviour)
- Cannot vote on your own reviews

**Saved units**
- Bookmark any unit with a single click
- Dedicated `/saved-units` page showing all bookmarked units
- Save state persists across sessions

**Profile pages**
- Public profile at `/profile/<username>`
- Stats summary — reviews written, average rating given, helpful votes received
- Full list of reviews by that user with links to the units
- Email visible only on own profile

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend framework | Flask 3 |
| Database | SQLite via SQLAlchemy ORM |
| Migrations | Flask-Migrate (Alembic) |
| Authentication | Flask-Login + werkzeug password hashing |
| Forms/CSRF | Flask-WTF + WTForms |
| Templating | Jinja2 |
| Frontend CSS | Bootstrap 5 + custom CSS |
| Frontend JS | jQuery + AJAX |
| Charts | Chart.js (loaded via CDN, only on unit detail page) |
| Icons | Font Awesome 6 |
| Fonts | Google Fonts (Inter) |

All chosen technologies are within the project brief's allowed list.

---

## Security

- **Passwords stored as salted hashes** using `werkzeug.security.generate_password_hash` (pbkdf2). Plaintext passwords are never stored.
- **CSRF protection** on every form via Flask-WTF, including AJAX requests via the `X-CSRFToken` header.
- **SQL injection prevention** through SQLAlchemy ORM — no raw SQL anywhere in the codebase.
- **XSS protection** via Jinja2's auto-escaping (default).
- **Secret key** read from environment variable in production, with a development fallback in `config.py`.

---

## How to Run the Application

### 1. Clone the repository
```bash
git clone https://github.com/nisorathiya/uwa-unireview.git
cd uwa-unireview
```

### 2. Create and activate a virtual environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialise the database
```bash
flask db upgrade
```

This creates `instance/unireview.db` with all required tables.

### 5. Seed the database with 32 UWA units
```bash
python3 seed.py
```

The script is safe to run multiple times— it skips units that already exists.

### 6. Run the server
```bash
python3 run.py
```

Open **http://localhost:5000** in your browser.


## How to Run the Tests


## Project Structure

```
uwa-unireview/
├── app/
│   ├── __init__.py            # App factory and extension setup
│   ├── models.py              # MODELS — SQLAlchemy database models
│   ├── routes.py              # CONTROLLERS — HTTP request handlers
│   ├── forms.py               # WTForms validation classes
│   ├── templates/             # VIEWS — Jinja2 HTML templates
│   └── static/                # VIEWS — CSS, JavaScript, images
├── migrations/                # Alembic migration scripts
├── instance/                  # SQLite database (gitignored)
├── docs/                      # Documentation
├── config.py                  # App configuration
├── run.py                     # Entry point
└── seed.py                    # Database seed script
```


## Database

Five tables managed via SQLAlchemy:

- **users** — registered student accounts
- **units** — UWA units (seeded from `seed.py`)
- **reviews** — student reviews of units
- **votes** — upvote/downvote on reviews
- **saved_units** — bookmarked units per user

For full schema details and ER diagram, see [`docs/DATABASE.md`](docs/DATABASE.md).

---

## Notes for Developers

- Always activate the virtual environment before running the app
- You will see `(venv)` at the start of your terminal line when it is active
- Never commit the `venv/` folder — it is in `.gitignore`
- Never commit the `instance/` folder — the database is local-only
- Run `git pull` before starting work each day to get the latest changes from teammates
- For new database schema changes, run `flask db migrate -m "description"` then `flask db upgrade`

---

## License

Academic project for CITS3403 Agile Web Development at the University of Western Australia.