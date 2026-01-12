"""
Integration test script for auth flow
Tests signup, signin, and task operations with JWT tokens
"""

import requests
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"
TEST_EMAIL = f"test-{datetime.now().timestamp()}@example.com"
TEST_PASSWORD = "TestPassword123!"

def print_step(step: str):
    print(f"\n{'='*60}")
    print(f"STEP: {step}")
    print(f"{'='*60}")

def print_result(success: bool, message: str, data=None):
    status = "SUCCESS" if success else "FAILED"
    print(f"[{status}] {message}")
    if data:
        print(f"Data: {json.dumps(data, indent=2)}")

# Test 1: Health Check
print_step("1. Health Check")
try:
    response = requests.get(f"{API_URL}/health")
    print_result(response.status_code == 200, "Health check", response.json())
except Exception as e:
    print_result(False, f"Health check failed: {str(e)}")
    exit(1)

# Test 2: Signup
print_step("2. User Signup")
auth_token = None
user_id = None

try:
    response = requests.post(
        f"{API_URL}/api/auth/sign-up/email",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )
    if response.status_code == 201:
        data = response.json()
        auth_token = data.get("access_token")
        user_id = data.get("user_id")
        print_result(True, "Signup successful", {
            "email": TEST_EMAIL,
            "user_id": user_id,
            "token_type": data.get("token_type")
        })
    else:
        print_result(False, f"Signup failed (Status {response.status_code})", response.json())
except Exception as e:
    print_result(False, f"Signup error: {str(e)}")

# Test 3: Login
print_step("3. User Login")
login_token = None

try:
    response = requests.post(
        f"{API_URL}/api/auth/login/email",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )
    if response.status_code == 200:
        data = response.json()
        login_token = data.get("access_token")
        print_result(True, "Login successful", {
            "email": TEST_EMAIL,
            "user_id": data.get("user_id"),
            "token_type": data.get("token_type")
        })
    else:
        print_result(False, f"Login failed (Status {response.status_code})", response.json())
except Exception as e:
    print_result(False, f"Login error: {str(e)}")

# Test 4: Verify Token
print_step("4. Token Verification")
if auth_token:
    try:
        response = requests.get(
            f"{API_URL}/api/auth/verify",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Token verification successful", data)
        else:
            print_result(False, f"Token verification failed (Status {response.status_code})", response.json())
    except Exception as e:
        print_result(False, f"Token verification error: {str(e)}")

# Test 5: Create Task (requires authentication)
print_step("5. Create Task with Auth")
if auth_token:
    try:
        response = requests.post(
            f"{API_URL}/api/tasks",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "title": "Test Task",
                "description": "This is a test task"
            }
        )
        if response.status_code == 201:
            task_data = response.json()
            print_result(True, "Task created successfully", task_data)
        else:
            print_result(False, f"Task creation failed (Status {response.status_code})", response.json())
    except Exception as e:
        print_result(False, f"Task creation error: {str(e)}")

# Test 6: List Tasks
print_step("6. List Tasks")
if auth_token:
    try:
        response = requests.get(
            f"{API_URL}/api/tasks",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        if response.status_code == 200:
            tasks = response.json()
            print_result(True, f"Tasks retrieved (count: {len(tasks)})", tasks[:2] if tasks else [])
        else:
            print_result(False, f"Task listing failed (Status {response.status_code})", response.json())
    except Exception as e:
        print_result(False, f"Task listing error: {str(e)}")

# Test 7: Unauthorized Access (invalid token)
print_step("7. Unauthorized Access Test")
try:
    response = requests.get(
        f"{API_URL}/api/tasks",
        headers={"Authorization": "Bearer invalid_token"}
    )
    if response.status_code == 401:
        print_result(True, "Correctly rejected invalid token", response.json())
    else:
        print_result(False, f"Should have rejected invalid token (Status {response.status_code})", response.json())
except Exception as e:
    print_result(False, f"Unauthorized test error: {str(e)}")

# Test 8: Duplicate Signup
print_step("8. Duplicate Email Signup Test")
try:
    response = requests.post(
        f"{API_URL}/api/auth/sign-up/email",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )
    if response.status_code == 409:
        print_result(True, "Correctly rejected duplicate email", response.json())
    else:
        print_result(False, f"Should have rejected duplicate email (Status {response.status_code})", response.json())
except Exception as e:
    print_result(False, f"Duplicate signup test error: {str(e)}")

# Test 9: Invalid Password
print_step("9. Invalid Password Test")
try:
    response = requests.post(
        f"{API_URL}/api/auth/login/email",
        json={
            "email": TEST_EMAIL,
            "password": "WrongPassword123!"
        }
    )
    if response.status_code == 401:
        print_result(True, "Correctly rejected invalid password", response.json())
    else:
        print_result(False, f"Should have rejected invalid password (Status {response.status_code})", response.json())
except Exception as e:
    print_result(False, f"Invalid password test error: {str(e)}")

print_step("All Tests Complete")
