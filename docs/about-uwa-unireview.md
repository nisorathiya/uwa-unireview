# UWA UniReview

## Purpose

UWA UniReview is a community-driven web platform that allows University of Western Australia students to read and submit honest, structured reviews of units they have studied. Students can search and filter units by faculty or code, view aggregated rating scores across four dimensions (overall experience, workload, difficulty, and usefulness), and directly message other students whose reviews they found helpful.

The platform addresses a genuine gap: prospective students currently have no reliable, peer-sourced way to evaluate units before enrolling. UniReview fills that gap with data from the people who matter most — students who have actually taken the unit.

---

## Key Features

- **Unit search and browse** — searchable directory of UWA units, filterable by faculty
- **Structured reviews** — four rating dimensions: overall, workload, difficulty, and usefulness
- **Aggregated scores** — average scores displayed per unit with visual score bars
- **User accounts** — register, log in, log out; reviews tied to your account
- **Profile page** — view all your own reviews and saved units in one place
- **Student forum** — contact other students by posting questions for help
- **Helpful votes** — upvote reviews to surface the most useful ones

---

## Technical Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (ES6), Bootstrap 5, jQuery |
| Backend | Python, Flask, Flask-Login, Flask-SQLAlchemy, Flask-WTF |
| Database | SQLite via SQLAlchemy ORM |
| Communication | AJAX (jQuery) for search/filter/votes |
| Dev tools | Git, GitHub (private repo), GitHub Issues for task tracking |
| Testing | pytest for Flask routes and database models |
| Extras | Chart.js (rating distribution charts), Font Awesome (icons) |

---

## List of Pages

| # | Page | Route | Description |
|---|---|---|---|
| 1 | Login / Sign up | `/login` `/register` | Split-screen layout. Left panel shows preview reviews to entice sign-up. Right panel toggles between login and registration forms. Validates UWA email format. |
| 2 | Dashboard (unit browse) | `/` | Homepage. Hero search bar with AJAX live filtering. Faculty filter pills. Unit cards showing aggregated scores colour-coded by rating level. Sorted by highest overall rating by default. |
| 3 | Unit detail page | `/unit/<id>` | Individual unit page. Shows score cards and visual score bars across all four dimensions. Review submission form with star rating widget. Paginated list of all student reviews with helpful vote buttons and Message Student action. |
| 4 | Student profile | `/profile` | Personal dashboard. Avatar, name, and stats (reviews written, helpful votes received, messages). Two tabs: My Reviews (with edit/delete) and Saved Units. Login required. |
| 5 | Student forum | `/forum` | A question forum interface. Lists all current questions with the student names and any reply if already answered. Right panel shows full message thread with the selected student, anchored to the unit context that started the conversation. |

---

## Team Organisation

- Weekly meeting every **Tuesday, 10 AM – 12 PM**