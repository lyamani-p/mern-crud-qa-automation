import requests

BASE_URL = "http://localhost:4000/api"
EMAIL = "lyama@gmail.com"
PASSWORD = "123456789"

def register_test_user(session):
    register_payload = {
        "email": EMAIL,
        "password": PASSWORD,
        "name": "Test User"
    }
    res = session.post(f"{BASE_URL}/auth/register", json=register_payload)
    # If user already exists, backend might return 400 or 409 — ignore those
    if res.status_code not in [200, 201, 400, 409]:
        raise Exception(f"Failed to register test user: {res.status_code} {res.text}")

def test_full_task_crud_flow():
    session = requests.Session()
    register_test_user(session) 

    # 1. Login and get token from cookie
    login_payload = {"email": EMAIL, "password": PASSWORD}
    res = session.post(f"{BASE_URL}/auth/login", json=login_payload)
    assert res.status_code == 200, f"Login failed: {res.status_code} {res.text}"

    # Check token exists
    token = session.cookies.get("token")
    print(token)
    assert token, "❌ No token found in cookies"
    print("✅ Logged in with token:", token)

    # 2. Create a task (token will be included automatically via cookies)
    task_payload = {
        "title": "LYAMANI API Task",
        "description": "Created by LYAMANI",
        "date": "2025-07-24T00:00:00.000Z"
    }
    res = session.post(f"{BASE_URL}/tasks", json=task_payload, cookies={"token": token})
    assert res.status_code in [200, 201], f"❌ Create failed: {res.status_code} {res.text}"
    task_id = res.json()["_id"]
    print("✅ Task created:", res.json())

    # 3. Get tasks
    res = session.get(f"{BASE_URL}/tasks", cookies={"token": token})
    assert res.status_code == 200, f"❌ Get failed: {res.status_code} {res.text}"
    print("✅ Tasks retrieved:", res.json())

    # 4. Update task
    update_payload = {"title": "Updated Title"}
    res = session.put(f"{BASE_URL}/tasks/{task_id}", json=update_payload, cookies={"token": token})
    assert res.status_code == 200, f"❌ Update failed: {res.status_code} {res.text}"
    print("✅ Task updated:", res.json())

    # 5. Delete task
    res = session.delete(f"{BASE_URL}/tasks/{task_id}", cookies={"token": token})
    assert res.status_code == 204, f"❌ Delete failed: {res.status_code} {res.text}"
    print("✅ Task deleted")


def test_login_invalid_email_format():
    session = requests.Session()
    payload = {"email": "invalidemail", "password": PASSWORD}
    res = session.post(f"{BASE_URL}/auth/login", json=payload)
    assert res.status_code in [400, 401], f"Expected 400 or 401 but got {res.status_code}"

def test_login_wrong_password():
    session = requests.Session()
    payload = {"email": EMAIL, "password": "wrongpassword"}
    res = session.post(f"{BASE_URL}/auth/login", json=payload)
    assert res.status_code == 400, f"Expected 400 Unauthorized but got {res.status_code}"

def test_login_empty_credentials():
    session = requests.Session()
    payload = {"email": "", "password": ""}
    res = session.post(f"{BASE_URL}/auth/login", json=payload)
    assert res.status_code in [400, 401], f"Expected 400 or 401 but got {res.status_code}"

def test_create_task_no_token():
    session = requests.Session()
    task_payload = {
        "title": "Test without token",
        "description": "Should fail",
        "date": "2025-07-24T00:00:00.000Z"
    }
    res = session.post(f"{BASE_URL}/tasks", json=task_payload)  # No token cookie
    assert res.status_code == 401, f"Expected 401 Unauthorized but got {res.status_code}"

def test_create_task_invalid_token():
    session = requests.Session()
    task_payload = {
        "title": "Test with invalid token",
        "description": "Should fail",
        "date": "2025-07-24T00:00:00.000Z"
    }
    res = session.post(f"{BASE_URL}/tasks", json=task_payload, cookies={"token": "invalidtoken"})
    assert res.status_code in [401, 403], f"Expected 401 or 403 but got {res.status_code}"

def test_create_task_missing_title():
    session = requests.Session()
    # Login first
    login_payload = {"email": EMAIL, "password": PASSWORD}
    res_login = session.post(f"{BASE_URL}/auth/login", json=login_payload)
    token = session.cookies.get("token")
    assert token, "No token found on login"

    # Create task with missing title
    task_payload = {
        "description": "Missing title field",
        "date": "2025-07-24T00:00:00.000Z"
    }
    res = session.post(f"{BASE_URL}/tasks", json=task_payload, cookies={"token": token})
    assert res.status_code == 400, f"Expected 400 Bad Request but got {res.status_code}"

def test_create_task_invalid_date_format():
    session = requests.Session()
    login_payload = {"email": EMAIL, "password": PASSWORD}
    res_login = session.post(f"{BASE_URL}/auth/login", json=login_payload)
    token = session.cookies.get("token")
    assert token, "No token found on login"

    task_payload = {
        "title": "Invalid date test",
        "description": "Bad date format",
        "date": "2020"
    }
    res = session.post(f"{BASE_URL}/tasks", json=task_payload, cookies={"token": token})
    assert res.status_code == 400, f"Expected 400 Bad Request but got {res.status_code}"


def test_update_task_nonexistent():
    session = requests.Session()
    login_payload = {"email": EMAIL, "password": PASSWORD}
    session.post(f"{BASE_URL}/auth/login", json=login_payload)
    token = session.cookies.get("token")
    assert token, "No token found on login"

    fake_task_id = "64e1234567890abcdef12345"  # Random/fake id
    update_payload = {"title": "Trying to update non-existent task"}
    res = session.put(f"{BASE_URL}/tasks/{fake_task_id}", json=update_payload, cookies={"token": token})
    assert res.status_code in [200, 404], f"Expected 404 Not Found but got {res.status_code}"

def test_delete_task_nonexistent():
    session = requests.Session()
    login_payload = {"email": EMAIL, "password": PASSWORD}
    session.post(f"{BASE_URL}/auth/login", json=login_payload)
    token = session.cookies.get("token")
    assert token, "No token found on login"

    fake_task_id = "64e1234567890abcdef12345"  # Random/fake id
    res = session.delete(f"{BASE_URL}/tasks/{fake_task_id}", cookies={"token": token})
    assert res.status_code == 404, f"Expected 404 Not Found but got {res.status_code}"