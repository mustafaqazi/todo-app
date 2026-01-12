"""Test password validation locally"""
import sys
sys.path.insert(0, '/backend')

from src.utils.password import validate_password_strength

test_passwords = [
    "TestPassword123!",  # Frontend test password
    "Test123",           # Too short
    "testpassword123",   # No uppercase
    "TESTPASSWORD123",   # No lowercase
    "TestPassword",      # No digit
    "TestPass123",       # Valid
]

print("Testing password validation:\n")
for password in test_passwords:
    is_valid, message = validate_password_strength(password)
    status = "PASS" if is_valid else "FAIL"
    print(f"[{status}] {password:20} -> {message}")
