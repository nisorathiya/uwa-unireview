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