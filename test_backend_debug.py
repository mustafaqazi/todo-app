"""
Debug script to test backend connectivity and identify issues
"""

import sys
import time
import subprocess
import requests
import json
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# Configuration
API_URL = "http://localhost:8000"
BACKEND_DIR = Path(__file__).parent / "backend"
TEST_EMAIL = "debug-test@example.com"
TEST_PASSWORD = "TestPassword123!"

print_section("Backend Debug Test")

# Step 1: Check if backend is running
print("\n[1] Checking if backend is running...")
try:
    response = requests.get(f"{API_URL}/health", timeout=2)
    print(f"✓ Backend is running (Status: {response.status_code})")
    print(f"  Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("✗ Backend is NOT running at http://localhost:8000")
    print("\nStarting backend...")

    # Start backend in subprocess
    backend_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(BACKEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for backend to start
    print("  Waiting for backend to start (10 seconds)...")
    time.sleep(10)

    # Check if it's running now
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        print(f"✓ Backend started successfully (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("✗ Backend failed to start")
        print("\nBackend stdout:")
        stdout, stderr = backend_process.communicate(timeout=1)
        print(stdout[:1000] if stdout else "  (no output)")
        print("\nBackend stderr:")
        print(stderr[:1000] if stderr else "  (no output)")
        sys.exit(1)
except Exception as e:
    print(f"✗ Error checking backend: {str(e)}")

# Step 2: Test signup endpoint
print_section("Testing Signup Endpoint")

try:
    print(f"\nSending POST /api/auth/sign-up/email")
    print(f"  Email: {TEST_EMAIL}")
    print(f"  Password: {TEST_PASSWORD}")

    response = requests.post(
        f"{API_URL}/api/auth/sign-up/email",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
        timeout=5
    )

    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")

    try:
        data = response.json()
        print(f"Response Body: {json.dumps(data, indent=2)}")

        if response.status_code == 201:
            print("\n✓ Signup successful!")
        elif response.status_code == 500:
            print("\n✗ Server error (500)")
            print("  This is likely a backend exception. Check backend logs.")
        else:
            print(f"\n✗ Unexpected status: {response.status_code}")
    except:
        print(f"Response Body (raw): {response.text[:500]}")

except requests.exceptions.Timeout:
    print("\n✗ Request timeout - backend might be slow or hanging")
except requests.exceptions.ConnectionError as e:
    print(f"\n✗ Connection error: {str(e)}")
except Exception as e:
    print(f"\n✗ Error: {str(e)}")

print_section("Debug Test Complete")
print("\nNext steps:")
print("1. Check the backend logs above for detailed error messages")
print("2. Ensure all environment variables are set (BETTER_AUTH_SECRET, DATABASE_URL)")
print("3. Verify the database is accessible")
print("4. Run: cd backend && python -m uvicorn main:app --reload")
