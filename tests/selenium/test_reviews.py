"""
Selenium tests: reviews and saved units.

These tests cover authenticated-user actions on the unit detail page:
submitting a review through the slider-based form, and toggling the
'save unit' bookmark via AJAX.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _set_slider_value(driver, slider_id, value):
    """Set a range-input slider's value via JS and dispatch input events.

    Selenium's send_keys doesn't reliably move <input type="range">, so
    we set the value programmatically and fire 'input' + 'change' so any
    jQuery handlers (which update the visible "3/5" labels) still run.
    """
    driver.execute_script(
        """
        const el = document.getElementById(arguments[0]);
        el.value = arguments[1];
        el.dispatchEvent(new Event('input',  { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        """,
        slider_id, str(value)
    )


def test_logged_in_user_can_submit_review(logged_in_driver, live_server):
    """A logged-in user can write and submit a review on a unit page,
    and the new review appears in the reviews list."""

    driver = logged_in_driver
    driver.get(f'{live_server}/unit/CITS3403')

    # Open the (initially hidden) review form.
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-toggle-review-form'))
    ).click()

    # The form lives inside #review-form; wait for its textarea to be visible.
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#review-form textarea[name="comment"]')
        )
    )

    # Move all four sliders to known values.
    _set_slider_value(driver, 'slider-overall',    5)
    _set_slider_value(driver, 'slider-workload',   4)
    _set_slider_value(driver, 'slider-difficulty', 3)
    _set_slider_value(driver, 'slider-usefulness', 5)

    # Fill in the comment (must be ≥ 20 chars to pass server-side validation).
    comment_text = 'Excellent unit, learned a great deal from the group project.'
    driver.find_element(
        By.CSS_SELECTOR, '#review-form textarea[name="comment"]'
    ).send_keys(comment_text)

    # Submit. The form posts to /review/submit which redirects back here.
    # Use JS click() rather than a Selenium click — the sticky navbar
    # (z-index:100) plus the slideToggle animation make the submit button's
    # screen coordinates unreliable, causing intercepted clicks.
    # A JS .click() fires the event directly on the element with no
    # coordinate hit-testing, which is exactly what we need here.
    submit_btn = driver.find_element(
        By.CSS_SELECTOR, '#review-form button[type="submit"]'
    )
    driver.execute_script('arguments[0].click();', submit_btn)

    # After submission a new .review-card should appear with our comment.
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.review-card'))
    )
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    assert comment_text in body_text, \
        'Expected the submitted review comment to appear on the page'

    # The review count in the hero (".unit-hero-meta") should now read 1.
    meta_text = driver.find_element(By.CSS_SELECTOR, '.unit-hero-meta').text
    assert '1 review' in meta_text, \
        f'Expected "1 review" in unit meta, got: {meta_text!r}'


def test_logged_in_user_can_save_unit(logged_in_driver, live_server):
    """The 'Save unit' bookmark button toggles state via AJAX and persists."""

    driver = logged_in_driver
    driver.get(f'{live_server}/unit/CITS3403')

    # Find the save button (rendered only for authenticated users).
    save_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-save-btn'))
    )
    assert 'Save unit' in save_btn.text, \
        f'Initial state should be "Save unit", got: {save_btn.text!r}'

    # Click — JS posts to /api/save-unit and swaps the button text/class.
    save_btn.click()
    WebDriverWait(driver, 5).until(
        lambda d: 'Saved' in d.find_element(By.CSS_SELECTOR, '.js-save-btn').text
    )
    save_btn = driver.find_element(By.CSS_SELECTOR, '.js-save-btn')
    assert 'ur-btn-saved' in save_btn.get_attribute('class'), \
        'Saved button should have the "ur-btn-saved" CSS class'

    # Reload the page — the saved state should persist (server-side).
    driver.refresh()
    save_btn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.js-save-btn'))
    )
    assert 'Saved' in save_btn.text, \
        'Save state should persist across page reload'


def test_user_can_edit_their_own_review(logged_in_driver, live_server, seed_helper):
    """A user can edit their own existing review and the updated text appears
    on the page after submission."""

    driver = logged_in_driver

    # Look up the logged-in user's ID rather than hardcoding it, so the test
    # doesn't break if the seed order in conftest changes later.
    seleniumuser_id = seed_helper.get_user_id('seleniumuser')

    # Seed an existing review by seleniumuser so we have something to edit.
    seed_helper.add_review(
        user_id=seleniumuser_id,
        unit_code='CITS3403',
        overall=3,
        comment='Original review text before any edits are applied.',
    )

    driver.get(f'{live_server}/unit/CITS3403')

    # The Edit button is only shown to the review author.
    edit_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.js-edit-review'))
    )
    edit_btn.click()

    # Clicking edit pre-fills the form, shows it, and changes the action URL.
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#review-form textarea[name="comment"]')
        )
    )

    # Replace the comment with new text.
    new_comment = 'Updated review text after editing — much more detail now.'
    comment_box = driver.find_element(
        By.CSS_SELECTOR, '#review-form textarea[name="comment"]'
    )
    comment_box.clear()
    comment_box.send_keys(new_comment)

    # Move the overall slider too, so we exercise an actual edit not just text.
    _set_slider_value(driver, 'slider-overall', 5)

    # Submit using JS click (sticky navbar makes coordinate clicks unreliable).
    submit_btn = driver.find_element(
        By.CSS_SELECTOR, '#review-form button[type="submit"]'
    )
    driver.execute_script('arguments[0].click();', submit_btn)

    # After redirect, the updated comment should be on the page and the
    # original should be gone.
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), new_comment)
    )
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    assert new_comment in body_text, 'Updated comment should be visible'
    assert 'Original review text' not in body_text, \
        'Original comment should have been replaced'


def test_user_can_upvote_another_users_review(logged_in_driver, live_server, seed_helper):
    """A user can upvote another user's review — the count increments via
    AJAX and the button gains the active state."""

    driver = logged_in_driver

    # Seed a different user and have them write the review we'll vote on.
    other_user_id = seed_helper.add_user(
        username='otherstudent',
        email='otherstudent@student.uwa.edu.au',
    )
    seed_helper.add_review(
        user_id=other_user_id,
        unit_code='CITS3403',
        overall=4,
        comment='A review by another student that we will upvote in this test.',
    )

    driver.get(f'{live_server}/unit/CITS3403')

    # Locate the upvote (data-value="1") button on the seeded review.
    upvote_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.js-vote[data-value="1"]')
        )
    )

    # Initial count should be 0.
    initial_count = upvote_btn.find_element(By.CSS_SELECTOR, '.vote-count').text
    assert initial_count == '0', \
        f'Expected initial upvote count to be 0, got {initial_count!r}'

    # Click via JS to avoid any sticky-navbar interception (same reasoning as
    # the review-submit test).
    driver.execute_script('arguments[0].click();', upvote_btn)

    # Wait for the AJAX response to update the count to 1.
    WebDriverWait(driver, 5).until(
        lambda d: d.find_element(
            By.CSS_SELECTOR, '.js-vote[data-value="1"] .vote-count'
        ).text == '1'
    )

    # The button should now be marked active.
    upvote_btn = driver.find_element(By.CSS_SELECTOR, '.js-vote[data-value="1"]')
    assert upvote_btn.get_attribute('data-active') == 'true', \
        'Upvote button should have data-active="true" after clicking'