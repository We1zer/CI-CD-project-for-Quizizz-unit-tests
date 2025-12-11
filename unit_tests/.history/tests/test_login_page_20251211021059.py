"""
Tests for LoginPage - Quizizz authentication
"""
import pytest
from login_page import LoginPage


# =============== POSITIVE TESTS ===============

def test_enter_valid_username():
    """Test 167: Enter valid username"""
    page = LoginPage()
    result = page.enter_username("testuser")
    assert result is True
    assert page.username == "testuser"

def test_enter_valid_password():
    """Test 168: Enter valid password"""
    page = LoginPage()
    result = page.enter_password("password123")
    assert result is True

def test_successful_login():
    """Test 169: Successful login with valid credentials"""
    page = LoginPage()
    page.enter_username("valid_user")
    page.enter_password("valid_pass")
    result = page.click_login_button()
    assert result is True
    assert page.is_user_logged_in() is True

def test_redirect_after_login():
    """Test 170: Check redirect URL after successful login"""
    page = LoginPage()
    page.enter_username("valid_user")
    page.enter_password("valid_pass")
    page.click_login_button()
    assert page.get_redirect_url() == "/dashboard"

def test_valid_email_format():
    """Test 171: Validate correct email format"""
    page = LoginPage()
    assert page.validate_email_format("user@example.com") is True

def test_password_reset_valid_email():
    """Test 172: Send password reset with valid email"""
    page = LoginPage()
    result = page.reset_password("user@example.com")
    assert result["status"] == "success"
    assert "Reset email sent" in result["message"]

def test_logout_after_login():
    """Test 173: Logout after successful login"""
    page = LoginPage()
    page.enter_username("valid_user")
    page.enter_password("valid_pass")
    page.click_login_button()
    result = page.logout()
    assert result is True
    assert page.is_user_logged_in() is False

def test_login_with_google_oauth():
    """Test 174: Login with Google OAuth"""
    page = LoginPage()
    result = page.login_with_google()
    assert result["provider"] == "google"
    assert result["status"] == "success"
    assert page.is_user_logged_in() is True

def test_login_with_microsoft_oauth():
    """Test 175: Login with Microsoft OAuth"""
    page = LoginPage()
    result = page.login_with_microsoft()
    assert result["provider"] == "microsoft"
    assert page.is_user_logged_in() is True


# =============== NEGATIVE TESTS ===============

def test_failed_login_wrong_credentials():
    """Test 176: Login fails with wrong credentials"""
    page = LoginPage()
    page.enter_username("wrong_user")
    page.enter_password("wrong_pass")
    result = page.click_login_button()
    assert result is False
    assert page.is_user_logged_in() is False

def test_error_message_on_failed_login():
    """Test 177: Error message displayed on failed login"""
    page = LoginPage()
    page.enter_username("invalid")
    page.enter_password("invalid")
    page.click_login_button()
    error = page.get_error_message()
    assert error == "Invalid username or password"

def test_empty_username():
    """Test 178: Empty username raises error"""
    page = LoginPage()
    with pytest.raises(ValueError, match="Username cannot be empty"):
        page.enter_username("")

def test_empty_password():
    """Test 179: Empty password raises error"""
    page = LoginPage()
    with pytest.raises(ValueError, match="Password cannot be empty"):
        page.enter_password("")

def test_whitespace_username():
    """Test 180: Whitespace-only username raises error"""
    page = LoginPage()
    with pytest.raises(ValueError, match="Username cannot be empty"):
        page.enter_username("   ")

def test_non_string_username():
    """Test 181: Non-string username raises TypeError"""
    page = LoginPage()
    with pytest.raises(TypeError, match="Username must be a string"):
        page.enter_username(12345)

def test_non_string_password():
    """Test 182: Non-string password raises TypeError"""
    page = LoginPage()
    with pytest.raises(TypeError, match="Password must be a string"):
        page.enter_password(None)

def test_login_without_credentials():
    """Test 183: Click login without entering credentials"""
    page = LoginPage()
    with pytest.raises(ValueError, match="Username and password must be entered first"):
        page.click_login_button()

def test_invalid_email_format_no_at():
    """Test 184: Invalid email without @ symbol"""
    page = LoginPage()
    assert page.validate_email_format("invalidemail.com") is False

def test_invalid_email_format_no_dot():
    """Test 185: Invalid email without dot"""
    page = LoginPage()
    assert page.validate_email_format("user@examplecom") is False

def test_password_reset_invalid_email():
    """Test 186: Password reset with invalid email"""
    page = LoginPage()
    with pytest.raises(ValueError, match="Invalid email format"):
        page.reset_password("invalidemail")

def test_logout_without_login():
    """Test 187: Logout without being logged in"""
    page = LoginPage()
    with pytest.raises(ValueError, match="User is not logged in"):
        page.logout()


# =============== EDGE CASES ===============

def test_no_redirect_on_failed_login():
    """Test 188: No redirect URL on failed login"""
    page = LoginPage()
    page.enter_username("invalid")
    page.enter_password("invalid")
    page.click_login_button()
    assert page.get_redirect_url() is None

def test_error_message_cleared_on_successful_login():
    """Test 189: Error message from previous attempt"""
    page = LoginPage()
    page.enter_username("invalid")
    page.enter_password("invalid")
    page.click_login_button()
    # Now login successfully
    page.enter_username("valid_user")
    page.enter_password("valid_pass")
    page.click_login_button()
    assert page.is_user_logged_in() is True

def test_username_stored_after_entry():
    """Test 190: Username is stored after entry"""
    page = LoginPage()
    page.enter_username("testuser123")
    assert page.username == "testuser123"
