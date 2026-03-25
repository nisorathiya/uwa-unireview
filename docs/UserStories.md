# UWA UniReview — User Stories

Three roles interact with the platform: a **Guest** (not logged in), a **Student** (registered and logged in), and an **Admin** (manages the platform). Stories are grouped by role, reflecting what each type of user can actually do.

---

## Role 1 — Guest

> A guest is anyone who visits the site without an account or without being logged in. They can browse and read content but cannot contribute.

---

**US-01 — Register for an account**
As a guest, I want to register with my name, email, and password so that I can become a student member and access the full platform.

- Email must end in `@student.uwa.edu.au`
- Password is hashed before storage — never stored in plain text
- Duplicate emails are rejected with a clear error message
- Redirects to the dashboard on successful registration

---

**US-02 — Log in**
As a guest, I want to log in with my email and password so that I can access my personalised content and contribute to the platform.

- A session is created on successful login
- Invalid credentials display an error message without revealing which field is wrong
- Redirects to the originally intended page after login

---

**US-03 — Search for a unit**
As a guest, I want to search for a unit by name or unit code so that I can quickly find the unit I am looking for without browsing the full list.

- Search results update without a full page reload (AJAX)
- Matches on partial unit code or name
- Results show unit code, name, faculty, and overall score

---

**US-04 — Filter units by faculty**
As a guest, I want to filter units by faculty so that I can narrow results to my area of study.

- Faculty filter pills are available on the homepage
- Selecting a faculty filters the unit grid client-side without a page reload
- An "All" option resets the filter to show every unit

---

**US-05 — View a unit detail page**
As a guest, I want to view a unit's detail page so that I can read its aggregated scores and student reviews before deciding to enrol.

- Unit detail page loads with all aggregated scores and score bars across four dimensions
- All student reviews are displayed on the page
- Accessible without being logged in

---

**US-06 — Read other students' reviews**
As a guest, I want to read all reviews for a unit so that I can make an informed enrolment decision based on real student experiences.

- Reviews are displayed in order of helpful votes by default
- Each review shows the reviewer's username, semester taken, all four dimension scores, and comment text
- Accessible without being logged in

---

**US-07 — Browse the unit forum**
As a guest, I want to read forum posts and replies for a unit so that I can see what students are currently discussing about it.

- Forum thread is visible on the unit detail page below the reviews section
- Posts are displayed in chronological order with the newest at the top
- Each post shows the author's username, timestamp, and post content
- Accessible without being logged in

---

## Role 2 — Student

> A student is a registered user who is logged in. They can do everything a guest can do, plus contribute reviews, vote, post in the forum, and manage their profile.

---

**US-08 — Log out**
As a student, I want to log out so that my session is securely ended and my account is protected.

- Session is fully cleared on logout
- Redirected to the homepage
- All protected routes become inaccessible after logging out

---

**US-09 — Submit a review**
As a student, I want to submit a review for a unit with ratings across four dimensions so that other students can benefit from my honest experience.

- Star rating widget covers overall, workload, difficulty, and usefulness
- A text comment is required before submission
- Only one review per student per unit is allowed, enforced by a database constraint

---

**US-10 — Edit or delete my own review**
As a student, I want to edit or delete my own review so that I can keep my feedback accurate and up to date over time.

- Edit and delete buttons are visible only on my own reviews
- Ownership is verified server-side — not just on the frontend
- Deletion requires a confirmation step to prevent accidental removal

---

**US-11 — Upvote a helpful review**
As a student, I want to upvote a review I found helpful so that the most useful reviews rise to the top for other students.

- One vote per student per review is enforced
- The vote count updates without a page reload via AJAX
- The vote count is displayed clearly on each review card

---

**US-12 — Post in the unit forum**
As a student, I want to post a question or comment in a unit's forum so that I can start a discussion with other students about that unit.

- A text input and submit button are available on the unit detail page forum section
- Post appears immediately in the thread after submission without a full page reload
- Post is tied to the student's account and displays their username and timestamp
- Login is required to post — guests see a "log in to post" prompt instead

---

**US-13 — Reply to a forum post**
As a student, I want to reply to another student's forum post so that I can answer their question or continue the discussion.

- Each forum post has a reply button that opens an inline reply input
- Replies are nested under the original post
- Reply displays the student's username and timestamp
- Login is required to reply

---

**US-14 — Delete my own forum post**
As a student, I want to delete my own forum post or reply so that I can remove something I posted by mistake.

- Delete button is visible only on my own posts and replies
- Ownership is verified server-side
- Deletion requires a confirmation step

---

**US-15 — View my profile**
As a student, I want to view my profile page so that I can see all the reviews and forum posts I have written and track my contributions.

- Profile shows my avatar/initials, stats (reviews written, votes received, forum posts)
- Tabbed view between My Reviews and My Forum Posts
- Unauthenticated users are redirected to the login page

---

## Role 3 — Admin

> An admin is a trusted platform manager who maintains the quality and integrity of the platform. Admin features are planned for a future sprint.

---

**US-16 — Remove an inappropriate review**
As an admin, I want to delete any review that violates community guidelines so that the platform remains trustworthy and respectful.

- Admin can delete any review regardless of who wrote it
- Deleted reviews are removed from the unit page immediately
- Action is logged for audit purposes

---

**US-17 — Remove an inappropriate forum post**
As an admin, I want to delete any forum post or reply that violates community guidelines so that discussions remain constructive and on-topic.

- Admin can delete any post or reply regardless of who wrote it
- Deleted posts are removed from the thread immediately
- Action is logged for audit purposes

---

**US-18 — Add a new unit to the directory**
As an admin, I want to add new units to the platform so that the unit directory stays current with UWA's course offerings.

- Admin can create a new unit with code, name, faculty, and credit points
- New unit appears immediately on the dashboard
- Duplicate unit codes are rejected