import time
from playwright.sync_api import expect

BASE_URL = "http://localhost:5173"

def login(page):
    page.goto(BASE_URL)
    page.click("text=Login")
    page.fill('input[name="email"]', "lyama@gmail.com")
    page.fill('input[name="password"]', "123456789")
    page.click('button:has-text("Login")')
    expect(page).to_have_url(BASE_URL + "/tasks")

def test_create_task(page):
    login(page)
    page.click('a:has-text("Add Task")')
    page.fill('input[name="title"]', "My new automated task")
    page.fill('textarea[name="description"]', "This is created by LYAMANI for Testing")
    page.fill('input[name="date"]', '2026-05-05')
    page.click('button:has-text("Save")')
    page.goto(BASE_URL + "/tasks")
    text = page.locator("header.flex:has-text('My new automated task')").first.inner_text()
    print("First header text:", text)

    assert "My new automated task" in text

def test_edit_task(page):
    login(page)
    task = page.locator("div.bg-zinc-800:has-text('My new automated task')")
    page.click('a:has-text("Edit")')

    page.fill('input[name="title"]', "Updated Task")
    page.click('button:has-text("Save")')

def test_delete_task(page):
    login(page)
    task = page.locator("div.bg-zinc-800:has-text('My new automated task')")
    page.click('button:has-text("Delete")')

    flex_div = page.locator("div.flex.justify-center.items-center.p-10")
    text = flex_div.inner_text()
    print("Text inside flex div:", text)

    assert "My new automated task" not in text
