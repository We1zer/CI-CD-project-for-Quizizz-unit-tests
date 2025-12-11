using System;

namespace Quizizz.Core.Pages
{
    /// <summary>
    /// Represents the login page of the Quizizz application.
    /// Methods update internal state and validate input.  In a real
    /// implementation you would interact with UI elements via Selenium or
    /// another web automation framework.
    /// </summary>
    public class LoginPage
    {
        public string Username { get; private set; } = string.Empty;
        public string Password { get; private set; } = string.Empty;
        public bool IsLoggedIn { get; private set; }
        public string ErrorMessage { get; private set; } = string.Empty;

        public void EnterUsername(string username)
        {
            if (string.IsNullOrWhiteSpace(username))
            {
                throw new ArgumentException("Username cannot be empty");
            }
            Username = username;
        }

        public void EnterPassword(string password)
        {
            if (string.IsNullOrWhiteSpace(password))
            {
                throw new ArgumentException("Password cannot be empty");
            }
            Password = password;
        }

        public void ClickLogin()
        {
            if (string.IsNullOrWhiteSpace(Username) || string.IsNullOrWhiteSpace(Password))
            {
                ErrorMessage = "Username or password missing";
                throw new InvalidOperationException("Both username and password must be provided before logging in");
            }
            // In a real implementation you would submit the login form and
            // handle navigation to the dashboard.  Here we simply update state.
            IsLoggedIn = true;
        }

        public void Logout()
        {
            IsLoggedIn = false;
            Username = string.Empty;
            Password = string.Empty;
        }
    }
}