from playwright.sync_api import expect
import uuid

BASE_URL = "http://localhost:5173"

def test_register_user(page):
    page.goto(BASE_URL)
    page.click("text=Register")

    name = f"user_{uuid.uuid4().hex[:6]}"
    page.fill('input[name="username"]', name)
    email = name + "@test.com"
    password = "test12345"
    print("email is " , email)
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    page.fill('input[name="confirmPassword"]', password)
    page.locator('button.bg-indigo-500:has-text("Submit")').click()
    expect(page).to_have_url(BASE_URL + "/tasks")

def test_login_valid_credentials(page):
    # Use an existing account
    page.goto(BASE_URL)
    page.click("text=Login")
    page.fill('input[name="email"]', "lyama@gmail.com")
    page.fill('input[name="password"]', "123456789")
    page.click('button:has-text("Login")')

    expect(page).to_have_url(BASE_URL + "/tasks")

def test_login_invalid_credentials(page):
    page.goto(BASE_URL)
    page.click("text=Login")
    page.fill('input[name="email"]', "wrong@test.com")
    page.fill('input[name="password"]', "wrongpass")
    page.click('button:has-text("Login")')

    expect(page).to_have_url(BASE_URL + "/login")