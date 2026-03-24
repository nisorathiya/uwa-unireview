# UWA UniReview — User Stories

## Authentication

**US-01 — Register**
As a new student, I can register with my name, student email, and password so that I can access the platform.

- Email must be a valid format
- Password is hashed before storage — never stored in plain text
- Duplicate emails are rejected with a clear error message
- Redirects to the dashboard on successful registration

---

**US-02 — Log in**
As a registered student, I can log in with my email and password so that I can access the UniReview content.

- A session is created on successful login
- Invalid credentials display an error message without revealing which field is wrong
- Redirects to the originally intended page after login

---

**US-03 — Log out**
As a logged-in student, I can log out so that my session is securely ended.

- Session is fully cleared on logout
- User is redirected to the homepage
- All protected routes become inaccessible after logging out

---

## Browsing & Discovery

**US-04 — Search for a unit**
As a user, I can search for a unit by name or unit code so that I can quickly find the unit I am looking for.

- Search results update without a full page reload (AJAX)
- Matches on partial unit code or name
- Results show unit code, name, faculty, and overall score

---

**US-05 — Filter by faculty**
As a user, I can filter units by faculty so that I can narrow results to my area of study.

- Faculty filter pills are available on the homepage
- Selecting a faculty filters the unit grid client-side without a page reload

---

**US-06 — View a unit detail page**
As a user, I can click on a unit card to view its full detail page so that I can read reviews and scores or search and click on the .

- Unit detail page loads with all aggregated scores and score bars
- All student reviews are displayed on the page
- Accessible without being logged in

---

## Reviews

**US-07 — Submit a review**
As a logged-in student, I can submit a review for a unit with ratings across four dimensions so that others can benefit from my experience.

- Star rating widget covers overall, workload, difficulty, and usefulness
- A text comment is required before submission
- Only one review per user per unit is allowed, enforced by a database constraint

---

**US-08 — Read other students reviews**
As any visitor, I can read all reviews for a unit written by other students so that I can make an informed enrolment decision.

- Reviews are displayed in order of helpful votes by default
- Each review shows the reviewer's username, semester taken, all four dimension scores, and comment text
- Accessible without being logged in

---

**US-09 — Edit or delete my own review**
As a logged-in student, I can edit or delete my own review so that I can keep my feedback accurate over time.

- Edit and delete buttons are visible only on the logged-in user's own reviews
- Ownership is verified server-side — not just on the frontend
- Deletion requires a confirmation step to prevent accidental removal

---

**US-10 — Upvote a helpful review**
As a logged-in student, I can upvote a review I found helpful so that the most useful reviews rise to the top.

- One vote per user per review is enforced
- The vote count updates without a page reload via AJAX
- The vote count is displayed clearly on each review card

---

## Profile & Messaging

**US-11 — View my profile**
As a logged-in student, I can view my profile page to see all reviews I have written and my helpful vote tally.

- Profile shows avatar/initials, stats summary (reviews written, votes received, messages)
- Tabbed view between My Reviews and Saved Units
- Login is required — unauthenticated users are redirected to the login page

---

**US-12 — Message another student**
As a logged-in student, I can message another student whose review I found insightful so that I can ask follow-up questions.

- A "Message student" button appears on each review card
- Opens a direct message thread pre-contextualised with the unit name
- Messages are persisted in the database between sessions

---

**US-13 — View my message inbox**
As a logged-in student, I can view all my message conversations in one inbox so that I can keep track of my discussions.

- Inbox sidebar lists all conversations with a preview of the last message
- Selecting a conversation loads the full message thread
- Unread messages are visually indicated in the sidebar