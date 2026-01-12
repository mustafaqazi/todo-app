"""Complete auth and task flow test"""
import requests
import json
from datetime import datetime

base_url = "http://localhost:8000"
test_email = f"user-{int(datetime.now().timestamp())}@example.com"
test_password = "TestPassword123!"

print(f"\nTesting complete auth + task flow")
print(f"Email: {test_email}")
print(f"=" * 60)

# 1. Signup
print("\n1. SIGNUP")
r = requests.post(f"{base_url}/api/auth/sign-up/email",
    json={"email": test_email, "password": test_password})
print(f"Status: {r.status_code}")
if r.status_code == 201:
    signup_data = r.json()
    token = signup_data["access_token"]
    user_id = signup_data["user_id"]
    print(f"Token: {token[:50]}...")
    print(f"User ID: {user_id}")
else:
    print(f"Error: {r.json()}")
    exit(1)

# 2. Signin
print("\n2. SIGNIN")
r = requests.post(f"{base_url}/api/auth/login/email",
    json={"email": test_email, "password": test_password})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    login_data = r.json()
    print(f"Token matches: {login_data['access_token'] == token}")
    print(f"User ID: {login_data['user_id']}")
else:
    print(f"Error: {r.json()}")

# 3. Verify token
print("\n3. VERIFY TOKEN")
r = requests.get(f"{base_url}/api/auth/verify",
    headers={"Authorization": f"Bearer {token}"})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    verify_data = r.json()
    print(f"Valid: {verify_data['valid']}")
    print(f"User ID: {verify_data['user_id']}")
else:
    print(f"Error: {r.json()}")

# 4. Create task
print("\n4. CREATE TASK")
r = requests.post(f"{base_url}/api",
    headers={"Authorization": f"Bearer {token}"},
    json={"title": "Test Task", "description": "This is a test"})
print(f"Status: {r.status_code}")
if r.status_code == 201:
    task = r.json()
    task_id = task["id"]
    print(f"Task ID: {task_id}")
    print(f"Title: {task['title']}")
    print(f"User ID matches: {task['user_id'] == user_id}")
else:
    print(f"Error: {r.json()}")
    exit(1)

# 5. List tasks
print("\n5. LIST TASKS")
r = requests.get(f"{base_url}/api",
    headers={"Authorization": f"Bearer {token}"})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    tasks = r.json()
    print(f"Task count: {len(tasks)}")
    if tasks:
        print(f"First task: {tasks[0]['title']}")
else:
    print(f"Error: {r.json()}")

# 6. Update task
print("\n6. UPDATE TASK")
r = requests.put(f"{base_url}/api/{task_id}",
    headers={"Authorization": f"Bearer {token}"},
    json={"title": "Updated Task Title"})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    task = r.json()
    print(f"Updated title: {task['title']}")
else:
    print(f"Error: {r.json()}")

# 7. Toggle complete
print("\n7. TOGGLE COMPLETE")
r = requests.patch(f"{base_url}/api/{task_id}/complete",
    headers={"Authorization": f"Bearer {token}"})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    task = r.json()
    print(f"Completed: {task['completed']}")
else:
    print(f"Error: {r.json()}")

# 8. Delete task
print("\n8. DELETE TASK")
r = requests.delete(f"{base_url}/api/{task_id}",
    headers={"Authorization": f"Bearer {token}"})
print(f"Status: {r.status_code}")
if r.status_code == 204:
    print("Task deleted successfully")
else:
    print(f"Error: {r.json()}")

# 9. Test invalid token
print("\n9. INVALID TOKEN")
r = requests.get(f"{base_url}/api/tasks",
    headers={"Authorization": "Bearer invalid_token_12345"})
print(f"Status: {r.status_code}")
print(f"Should be 401: {r.status_code == 401}")

print("\n" + "=" * 60)
print("All tests completed!")
