"""
Selenium test: end-to-end register → login → logout flow.

Exercises the full authentication journey through the browser:
the user signs up via the registration form, sees the dashboard,
logs out, and then logs back in with the same credentials.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_register_login_logout_flow(driver, live_server):
    """A new student can register, log out, and log back in successfully."""

    # ─── 1. Open the login page and switch to the Sign-up tab ──────────────
    driver.get(f'{live_server}/login')

    # The page has two tab buttons; clicking 'tab-signup' reveals the
    # registration form (the JS swaps which form is visible).
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'tab-signup'))
    ).click()

    signup_form = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'form-signup'))
    )

    # ─── 2. Fill in the registration form and submit ───────────────────────
    signup_form.find_element(By.NAME, 'name').send_keys('Alice Tester')
    signup_form.find_element(By.NAME, 'email').send_keys('alicetester@student.uwa.edu.au')
    signup_form.find_element(By.NAME, 'password').send_keys('password123')
    signup_form.find_element(By.NAME, 'confirm').send_keys('password123')
    # WTForms renders SubmitField as <input type="submit">, not <button>
    signup_form.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    # After successful registration the user is logged in and redirected
    # to the dashboard. The dashboard has a search box with id "search-input".
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'search-input'))
    )
    assert '/login' not in driver.current_url, \
        'Expected redirect away from /login after successful registration'

    # ─── 3. Log out ────────────────────────────────────────────────────────
    driver.get(f'{live_server}/logout')

    # After logout the user is redirected to /login again.
    WebDriverWait(driver, 5).until(
        EC.url_contains('/login')
    )
    assert '/login' in driver.current_url

    # ─── 4. Log back in with the same credentials ──────────────────────────
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'form-login'))
    )
    login_form = driver.find_element(By.ID, 'form-login')
    login_form.find_element(By.NAME, 'email').send_keys('alicetester@student.uwa.edu.au')
    login_form.find_element(By.NAME, 'password').send_keys('password123')
    login_form.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    # Should land on the dashboard again
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'search-input'))
    )
    assert '/login' not in driver.current_url, \
        'Expected redirect away from /login after successful login'


def test_login_with_wrong_password_shows_error(driver, live_server):
    """Logging in with an incorrect password keeps the user on /login
    and displays an error message to the user."""

    driver.get(f'{live_server}/login')

    # Wait for the login form to be present and fill it with wrong creds.
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'form-login'))
    )
    login_form = driver.find_element(By.ID, 'form-login')
    login_form.find_element(By.NAME, 'email').send_keys('seleniumuser@student.uwa.edu.au')
    login_form.find_element(By.NAME, 'password').send_keys('definitely-not-the-right-password')
    login_form.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    # Wait for the toast that the login route renders on failure.
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.ur-toast-danger'))
    )

    # Should still be on /login (no redirect on failed login).
    assert '/login' in driver.current_url, \
        f'Expected to remain on /login after wrong password, got: {driver.current_url}'

    # The error message text should mention invalid credentials.
    alert_text = driver.find_element(By.CSS_SELECTOR, '.ur-toast-danger').text
    assert 'Invalid email or password' in alert_text, \
        f'Expected "Invalid email or password" toast, got: {alert_text!r}'