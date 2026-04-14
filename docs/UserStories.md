# UWA UniReview — User Stories

---

**Title:** User Registration
**User Story:** As a new student, I want to register with my name, email and password so that I can create an account and access the platform.
**Acceptance Criteria:**

- **Scenario 1:** Valid UWA email provided.
  - **Given** I am on the registration page
  - **When** I enter my name, a valid UWA student email and a password and click Sign up
  - **Then** my account is created and I am redirected to the dashboard

- **Scenario 2:** Email is already registered.
  - **Given** I am on the registration page
  - **When** I enter an email address that is already associated with an existing account
  - **Then** I receive an error message informing me that the email is already in use

- **Scenario 3:** Non-UWA email provided.
  - **Given** I am on the registration page
  - **When** I enter an email address that does not end in @student.uwa.edu.au
  - **Then** I receive an error message requesting that I use my UWA student email address

---

**Title:** User Login
**User Story:** As a registered student, I want to log in with my email and password so that I can access my account and use the platform.
**Acceptance Criteria:**

- **Scenario 1:** Correct credentials entered.
  - **Given** I am on the login page
  - **When** I enter my registered email address and correct password and click Log in
  - **Then** I am authenticated and redirected to the dashboard

- **Scenario 2:** Incorrect credentials entered.
  - **Given** I am on the login page
  - **When** I enter an incorrect email address or password
  - **Then** I receive an error message indicating that my credentials are invalid

---

**Title:** User Logout
**User Story:** As a logged-in student, I want to log out of my account so that my session is securely terminated when I am finished using the platform.
**Acceptance Criteria:**

- **Scenario 1:** Student logs out successfully.
  - **Given** I am logged in and viewing any page
  - **When** I click the Log out button in the navigation bar
  - **Then** my session is ended and I am redirected to the homepage

- **Scenario 2:** Accessing a protected page after logout.
  - **Given** I have logged out of my account
  - **When** I attempt to navigate to a protected page such as my profile
  - **Then** I am redirected to the login page

---

**Title:** Search and Filter Units
**User Story:** As a student, I want to search for a unit by name or code and filter by faculty so that I can locate a specific unit efficiently.
**Acceptance Criteria:**

- **Scenario 1:** Searching by unit name.
  - **Given** I am on the dashboard
  - **When** I type a unit name into the search bar
  - **Then** the unit grid updates immediately to display only matching results without a full page reload

- **Scenario 2:** Searching by unit code.
  - **Given** I am on the dashboard
  - **When** I enter a unit code such as CITS3403 into the search bar
  - **Then** only units matching that code are displayed

- **Scenario 3:** Filtering by faculty.
  - **Given** I am on the dashboard
  - **When** I select a faculty filter such as Engineering and Computing
  - **Then** the unit grid displays only units belonging to that faculty

- **Scenario 4:** No matching results found.
  - **Given** I am on the dashboard
  - **When** I enter a search term that does not match any unit
  - **Then** a message is displayed informing me that no units were found

---

**Title:** View Unit Detail Page
**User Story:** As a student, I want to view a unit's detail page so that I can review its aggregated scores and student reviews before making an enrolment decision.
**Acceptance Criteria:**

- **Scenario 1:** Viewing a unit with existing reviews.
  - **Given** I am on the dashboard
  - **When** I click on a unit card
  - **Then** I am taken to that unit's detail page displaying aggregated scores and all submitted reviews

- **Scenario 2:** Viewing a unit with no reviews.
  - **Given** I click on a unit that has not yet received any reviews
  - **When** the unit detail page loads
  - **Then** a message is displayed informing me that no reviews have been submitted yet

- **Scenario 3:** Viewing as an unauthenticated user.
  - **Given** I am not logged in
  - **When** I navigate to a unit detail page
  - **Then** I can view all scores and reviews without being required to log in

---

**Title:** Submit a Review
**User Story:** As a logged-in student, I want to submit a review for a unit so that other students can benefit from my experience when considering enrolment.
**Acceptance Criteria:**

- **Scenario 1:** Successfully submitting a review.
  - **Given** I am logged in and viewing a unit page for which I have not previously submitted a review
  - **When** I provide star ratings for all four dimensions, write a comment and click Submit
  - **Then** my review is saved and displayed on the unit page immediately

- **Scenario 2:** Submitting without a comment.
  - **Given** I am completing the review form
  - **When** I provide star ratings but leave the comment field empty and click Submit
  - **Then** I receive a validation error requesting that I write a comment before submitting

- **Scenario 3:** Attempting to review a unit twice.
  - **Given** I have already submitted a review for a unit
  - **When** I visit that unit's page again
  - **Then** the review submission form is not displayed and I am informed that I have already reviewed this unit

---

**Title:** Edit or Delete a Review
**User Story:** As a logged-in student, I want to edit or delete my own review so that I can ensure my feedback remains accurate and up to date.
**Acceptance Criteria:**

- **Scenario 1:** Editing an existing review.
  - **Given** I am logged in and viewing one of my own reviews
  - **When** I click Edit, modify the content and save my changes
  - **Then** my review is updated and the revised content is displayed on the unit page

- **Scenario 2:** Deleting an existing review.
  - **Given** I am logged in and viewing one of my own reviews
  - **When** I click Delete and confirm the action
  - **Then** my review is permanently removed from the unit page

- **Scenario 3:** Attempting to edit another student's review.
  - **Given** I am logged in and viewing another student's review
  - **When** I view that review
  - **Then** no Edit or Delete buttons are displayed for that review

---

**Title:** Mark a Review as Helpful
**User Story:** As a logged-in student, I want to upvote a review I found useful so that the most helpful reviews are prioritised for other students.
**Acceptance Criteria:**

- **Scenario 1:** Upvoting a review.
  - **Given** I am logged in and reading a review that I did not author
  - **When** I click the upvote button
  - **Then** the vote count increments by one immediately without a full page reload

- **Scenario 2:** Removing an upvote.
  - **Given** I have previously upvoted a review
  - **When** I click the upvote button again
  - **Then** my vote is withdrawn and the count decrements accordingly

- **Scenario 3:** Attempting to upvote an own review.
  - **Given** I am logged in and viewing a review I authored
  - **When** I view the upvote button
  - **Then** the button is disabled and I am unable to vote on my own review

---

**Title:** Save a Unit
**User Story:** As a logged-in student, I want to save units I am interested in so that I can revisit them easily from my profile page.
**Acceptance Criteria:**

- **Scenario 1:** Saving a unit.
  - **Given** I am logged in and viewing a unit card or unit detail page
  - **When** I click the Save button
  - **Then** the unit is added to my saved units list on my profile page

- **Scenario 2:** Removing a saved unit.
  - **Given** I have previously saved a unit
  - **When** I click the Save button again on that unit
  - **Then** the unit is removed from my saved units list

- **Scenario 3:** Viewing saved units while not logged in.
  - **Given** I am not logged in
  - **When** I attempt to save a unit
  - **Then** I am redirected to the login page

---

**Title:** View Personal Profile
**User Story:** As a logged-in student, I want to view my profile page so that I can manage my reviews and saved units in one place.
**Acceptance Criteria:**

- **Scenario 1:** Viewing submitted reviews.
  - **Given** I am logged in and on my profile page
  - **When** I select the My Reviews tab
  - **Then** all reviews I have submitted are displayed with options to edit or delete each one

- **Scenario 2:** Viewing saved units.
  - **Given** I am logged in and on my profile page
  - **When** I select the Saved Units tab
  - **Then** all units I have saved are displayed with links to their detail pages

- **Scenario 3:** Accessing the profile page while not logged in.
  - **Given** I am not logged in
  - **When** I attempt to navigate to the profile page
  - **Then** I am redirected to the login page