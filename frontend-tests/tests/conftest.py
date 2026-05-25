import pytest

from playwright.sync_api import sync_playwright
from config.environment_data import urls

def pytest_addoption(parser):
    """Add mandatory parameter needed to be provided through command line"""
    parser.addoption("--env", required=True, choices=["demo"], help="Please provide on which environment to run tests")

@pytest.fixture
def get_environment(request):
    """Method to return environment variable passed in command line"""
    return request.config.getoption("--env")

def get_base_url(environment):
    """Method to return base url to be used in tests"""
    return urls[environment]

@pytest.fixture(scope="function")
def browser_page():
    """Base fixture to manage browser lifecycle"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        yield page

        page.close()
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def setup_shop(browser_page, get_environment):
    """
    Initializes the browser, opens the store URL directly, and returns the ready-to-use page context to the test.
    """
    base_url=get_base_url(get_environment)
    browser_page.goto(base_url, timeout=15000)
    return browser_page