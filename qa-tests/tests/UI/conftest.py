import pytest
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chromium", help="Browser to use (chromium, firefox, webkit)")
    parser.addoption("--headed", action="store_true", help="Run browser in headed mode")

@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=not headed)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
