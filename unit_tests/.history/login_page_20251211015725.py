"""
LoginPage - Page Object для сторінки авторизації Quizizz
"""

class LoginPage:
    """Quizizz Login page - authentication functionality"""
    
    def __init__(self):
        self.is_logged_in = False
        self.username = None
        self.error_message = None
        self.redirect_url = None
    
    def enter_username(self, username):
        """Enter username in login form"""
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not username.strip():
            raise ValueError("Username cannot be empty")
        self.username = username
        return True
    
    def enter_password(self, password):
        """Enter password in login form"""
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if not password.strip():
            raise ValueError("Password cannot be empty")
        self.password = password
        return True
    
    def click_login_button(self):
        """Click login button"""
        if not hasattr(self, 'username') or not hasattr(self, 'password'):
            raise ValueError("Username and password must be entered first")
        
        # Simulate login validation
        if self.username == "valid_user" and self.password == "valid_pass":
            self.is_logged_in = True
            self.redirect_url = "/dashboard"
            return True
        else:
            self.error_message = "Invalid username or password"
            return False
    
    def get_error_message(self):
        """Get error message if login failed"""
        return self.error_message
    
    def is_user_logged_in(self):
        """Check if user is logged in"""
        return self.is_logged_in
    
    def get_redirect_url(self):
        """Get redirect URL after successful login"""
        return self.redirect_url
    
    def validate_email_format(self, email):
        """Validate email format"""
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        if '@' not in email or '.' not in email:
            return False
        return True
    
    def reset_password(self, email):
        """Send password reset email"""
        if not self.validate_email_format(email):
            raise ValueError("Invalid email format")
        return {"status": "success", "message": "Reset email sent"}
    
    def logout(self):
        """Logout current user"""
        if not self.is_logged_in:
            raise ValueError("User is not logged in")
        self.is_logged_in = False
        self.username = None
        self.password = None
        self.redirect_url = None
        return True
    
    def login_with_google(self):
        """Login with Google OAuth"""
        self.is_logged_in = True
        self.redirect_url = "/dashboard"
        return {"provider": "google", "status": "success"}
    
    def login_with_microsoft(self):
        """Login with Microsoft OAuth"""
        self.is_logged_in = True
        self.redirect_url = "/dashboard"
        return {"provider": "microsoft", "status": "success"}
