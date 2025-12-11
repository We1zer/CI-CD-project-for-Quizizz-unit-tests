using System;
using Quizizz.Core.Pages;
using Xunit;

namespace Quizizz.Tests.Pages
{
    public class LoginPageTests
    {
        [Fact]
        public void EnterUsername_ValidInput_SetsProperty()
        {
            var page = new LoginPage();
            page.EnterUsername("user1");
            Assert.Equal("user1", page.Username);
        }

        [Fact]
        public void EnterUsername_Empty_Throws()
        {
            var page = new LoginPage();
            Assert.Throws<ArgumentException>(() => page.EnterUsername(""));
        }

        [Fact]
        public void EnterPassword_ValidInput_SetsProperty()
        {
            var page = new LoginPage();
            page.EnterPassword("pass123");
            Assert.Equal("pass123", page.Password);
        }

        [Fact]
        public void EnterPassword_Empty_Throws()
        {
            var page = new LoginPage();
            Assert.Throws<ArgumentException>(() => page.EnterPassword("   "));
        }

        [Fact]
        public void ClickLogin_WithCredentials_SetsLoggedIn()
        {
            var page = new LoginPage();
            page.EnterUsername("user");
            page.EnterPassword("pass");
            page.ClickLogin();
            Assert.True(page.IsLoggedIn);
        }

        [Fact]
        public void ClickLogin_WithoutCredentials_Throws()
        {
            var page = new LoginPage();
            var ex = Assert.Throws<InvalidOperationException>(() => page.ClickLogin());
            Assert.Equal("Both username and password must be provided before logging in", ex.Message);
            Assert.False(page.IsLoggedIn);
        }

        [Fact]
        public void Logout_ClearsState()
        {
            var page = new LoginPage();
            page.EnterUsername("user");
            page.EnterPassword("pass");
            page.ClickLogin();
            page.Logout();
            Assert.False(page.IsLoggedIn);
            Assert.Equal(string.Empty, page.Username);
            Assert.Equal(string.Empty, page.Password);
        }
    }
}