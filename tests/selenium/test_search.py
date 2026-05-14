"""
Selenium tests: dashboard search and faculty filter.

The dashboard injects unit cards via AJAX (jQuery → /api/search),
debounced 220 ms after each keystroke. These tests verify the
client-side filtering behaves correctly end-to-end through Chrome.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _wait_for_cards(driver, timeout=5):
    """Wait until at least one unit card has been rendered, then return
    the visible card elements."""
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.ur-unit-card'))
    )
    return driver.find_elements(By.CSS_SELECTOR, '.ur-unit-card')


def test_search_filters_units_by_keyword(driver, live_server):
    """Typing a unit code in the search box filters cards via AJAX."""

    driver.get(live_server + '/')

    # All seeded units appear on first load (3 of them).
    initial_cards = _wait_for_cards(driver)
    assert len(initial_cards) == 3, \
        f'Expected 3 seeded units on first load, got {len(initial_cards)}'

    # Type a code that matches exactly one unit. The dashboard debounces
    # for 220 ms, so we wait for the count to drop.
    search = driver.find_element(By.ID, 'search-input')
    search.clear()
    search.send_keys('CITS3403')

    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, '.ur-unit-card')) == 1
    )
    cards = driver.find_elements(By.CSS_SELECTOR, '.ur-unit-card')
    assert 'CITS3403' in cards[0].text, \
        f'Expected the only card to be CITS3403, got: {cards[0].text!r}'


def test_faculty_filter_pill_narrows_results(driver, live_server):
    """Clicking the 'Science' filter pill shows only science units."""

    driver.get(live_server + '/')

    # Wait for the initial AJAX load to complete.
    _wait_for_cards(driver)

    # Click the Science faculty pill.
    science_pill = driver.find_element(
        By.CSS_SELECTOR, '.ur-filter-pill[data-faculty="Science"]'
    )
    science_pill.click()

    # We seeded exactly one Science unit (PSYC1101).
    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, '.ur-unit-card')) == 1
    )
    cards = driver.find_elements(By.CSS_SELECTOR, '.ur-unit-card')
    assert 'PSYC1101' in cards[0].text, \
        f'Expected PSYC1101 after Science filter, got: {cards[0].text!r}'

    # The clicked pill should now be marked active.
    assert 'active' in science_pill.get_attribute('class'), \
        'Science pill should have the "active" class after clicking'