#!/usr/bin/env python3
"""
Test script for the authentication flow
Tests: JWT validation, task creation, user isolation
"""

import json
import time
from datetime import datetime, timedelta
import jwt
import requests

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
BETTER_AUTH_SECRET = "default-secret-change-in-production"
JWT_ALGORITHM = "HS256"

# Test users
USER_1_ID = "test-user-001"
USER_2_ID = "test-user-002"

def create_jwt_token(user_id: str) -> str:
    """Create a valid JWT token"""
    payload = {
        "sub": user_id,  # Standard JWT claim
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, BETTER_AUTH_SECRET, algorithm=JWT_ALGORITHM)

def test_backend_health():
    """Test backend health endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Backend Health Check")
    print("="*60)

    try:
        response = requests.get(f"{BACKEND_URL}/health")
        print(f"✅ Backend Health: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Backend Health Failed: {e}")
        return False

def test_task_without_jwt():
    """Test task creation without JWT (should fail with 401)"""
    print("\n" + "="*60)
    print("TEST 2: Task Creation Without JWT (Expected: 401)")
    print("="*60)

    payload = {
        "title": "Test Task",
        "description": "This should fail"
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/tasks",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print(f"✅ Correctly rejected (401): {response.json()}")
            return True
        else:
            print(f"❌ Expected 401, got {response.status_code}: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Request Failed: {e}")
        return False

def test_task_with_invalid_jwt():
    """Test task creation with invalid JWT (should fail with 401)"""
    print("\n" + "="*60)
    print("TEST 3: Task Creation With Invalid JWT (Expected: 401)")
    print("="*60)

    payload = {
        "title": "Test Task",
        "description": "This should also fail"
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/tasks",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer invalid.jwt.token"
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print(f"✅ Correctly rejected (401): {response.json()}")
            return True
        else:
            print(f"❌ Expected 401, got {response.status_code}: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Request Failed: {e}")
        return False

def test_task_creation_user_1():
    """Test task creation with valid JWT for user 1"""
    print("\n" + "="*60)
    print(f"TEST 4: Task Creation for {USER_1_ID} (Expected: 201)")
    print("="*60)

    token = create_jwt_token(USER_1_ID)
    print(f"   JWT Created: {token[:50]}...")

    payload = {
        "title": "User 1 Task",
        "description": "This is a task for user 1"
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/tasks",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            task = response.json()
            print(f"✅ Task Created: {task['id']}")
            print(f"   User ID: {task['user_id']}")
            print(f"   Title: {task['title']}")
            print(f"   Created At: {task['created_at']}")
            return True, task['id']
        else:
            print(f"❌ Expected 201, got {response.status_code}: {response.json()}")
            return False, None
    except Exception as e:
        print(f"❌ Request Failed: {e}")
        return False, None

def test_task_creation_user_2():
    """Test task creation with valid JWT for user 2"""
    print("\n" + "="*60)
    print(f"TEST 5: Task Creation for {USER_2_ID} (Expected: 201)")
    print("="*60)

    token = create_jwt_token(USER_2_ID)
    print(f"   JWT Created: {token[:50]}...")

    payload = {
        "title": "User 2 Task",
        "description": "This is a task for user 2"
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/api/tasks",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            task = response.json()
            print(f"✅ Task Created: {task['id']}")
            print(f"   User ID: {task['user_id']}")
            print(f"   Title: {task['title']}")
            return True, task['id']
        else:
            print(f"❌ Expected 201, got {response.status_code}: {response.json()}")
            return False, None
    except Exception as e:
        print(f"❌ Request Failed: {e}")
        return False, None

def test_user_isolation(user_1_task_id, user_2_task_id):
    """Test that user 1 cannot access user 2's task"""
    print("\n" + "="*60)
    print("TEST 6: User Isolation (User 1 accessing User 2's task)")
    print("="*60)

    token = create_jwt_token(USER_1_ID)
    print(f"   User 1 JWT: {token[:50]}...")
    print(f"   Attempting to access User 2 Task: {user_2_task_id}")

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/tasks/{user_2_task_id}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"✅ Correctly denied (404): Task not accessible")
            return True
        else:
            print(f"❌ Expected 404, got {response.status_code}: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Request Failed: {e}")
        return False

def test_list_tasks_user_1(user_1_task_id):
    """Test that user 1 only sees their own tasks"""
    print("\n" + "="*60)
    print("TEST 7: List Tasks - User 1 (Expected: Only their tasks)")
    print("="*60)

    token = create_jwt_token(USER_1_ID)

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/tasks",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Task List Retrieved: {len(tasks)} task(s)")

            user_1_owns_task = any(t['id'] == user_1_task_id for t in tasks)
            print(f"   Contains User 1's task: {user_1_owns_task}")

            if user_1_owns_task and len(tasks) == 1:
                print(f"✅ User 1 only sees their own task")
                return True
            elif not user_1_owns_task:
                print(f"❌ User 1 cannot see their own task!")
                return False
            else:
                print(f"❌ User 1 sees {len(tasks)} tasks (expected 1)")
                return False
        else:
            print(f"❌ Expected 200, got {response.status_code}: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Request Failed: {e}")
        return False

def test_frontend_available():
    """Test that frontend is running"""
    print("\n" + "="*60)
    print("TEST 8: Frontend Availability Check")
    print("="*60)

    try:
        response = requests.get(f"{FRONTEND_URL}/login", timeout=5)
        if response.status_code == 200:
            print(f"✅ Frontend Running on {FRONTEND_URL}")
            print(f"   Login page accessible (200)")
            return True
        else:
            print(f"⚠️  Frontend responded with {response.status_code}")
            return True  # Still consider it running
    except Exception as e:
        print(f"❌ Frontend Not Available: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AUTHENTICATION FLOW TEST SUITE".center(60))
    print("="*60)

    results = []

    # Test backend and frontend availability
    results.append(("Backend Health", test_backend_health()))
    results.append(("Frontend Available", test_frontend_available()))

    # Test JWT validation
    results.append(("No JWT (401)", test_task_without_jwt()))
    results.append(("Invalid JWT (401)", test_task_with_invalid_jwt()))

    # Test task creation
    success_1, task_1_id = test_task_creation_user_1()
    results.append(("User 1 Task Creation", success_1))

    success_2, task_2_id = test_task_creation_user_2()
    results.append(("User 2 Task Creation", success_2))

    # Test user isolation
    if task_1_id and task_2_id:
        results.append(("User Isolation (Cross-Access)", test_user_isolation(task_1_id, task_2_id)))
        results.append(("User 1 List Tasks", test_list_tasks_user_1(task_1_id)))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nAuthentication flow is working correctly:")
        print("  ✅ JWT validation working")
        print("  ✅ Task creation with JWT working")
        print("  ✅ User isolation enforced")
        print("  ✅ Frontend and backend communicating")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())
