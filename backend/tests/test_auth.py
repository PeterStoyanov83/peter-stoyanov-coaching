#!/usr/bin/env python3
"""
Test authentication system
"""

from auth import verify_password, authenticate_user, SUPERUSER_PASSWORD_HASH

def test_authentication():
    """Test the authentication system"""
    
    print("🔐 Testing Authentication System")
    print("=" * 40)
    
    # Test password verification
    password = "CoachingMaster2024!"
    print(f"Testing password: {password}")
    print(f"Against hash: {SUPERUSER_PASSWORD_HASH}")
    
    is_valid = verify_password(password, SUPERUSER_PASSWORD_HASH)
    print(f"Password verification result: {is_valid}")
    
    if is_valid:
        print("✅ Password verification successful!")
    else:
        print("❌ Password verification failed!")
        
        # Let's try generating a new hash
        from auth import get_password_hash
        new_hash = get_password_hash(password)
        print(f"New hash generated: {new_hash}")
        
        # Test the new hash
        is_valid_new = verify_password(password, new_hash)
        print(f"New hash verification: {is_valid_new}")
    
    # Test full authentication
    print("\n🧪 Testing full authentication...")
    user = authenticate_user("peterstoyanov", password)
    
    if user:
        print("✅ Full authentication successful!")
        print(f"User: {user.username}, Admin: {user.is_admin}")
    else:
        print("❌ Full authentication failed!")
    
    # Test wrong password
    print("\n🧪 Testing wrong password...")
    wrong_user = authenticate_user("peterstoyanov", "wrongpassword")
    
    if not wrong_user:
        print("✅ Correctly rejected wrong password!")
    else:
        print("❌ Security issue - accepted wrong password!")

if __name__ == "__main__":
    test_authentication()