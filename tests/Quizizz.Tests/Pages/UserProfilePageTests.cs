using System;
using Quizizz.Core.Pages;
using Xunit;

namespace Quizizz.Tests.Pages
{
    public class UserProfilePageTests
    {
        [Fact]
        public void UpdateDisplayName_Valid_SetsName()
        {
            var page = new UserProfilePage();
            page.UpdateDisplayName("John");
            Assert.Equal("John", page.DisplayName);
        }

        [Fact]
        public void UpdateDisplayName_Invalid_Throws()
        {
            var page = new UserProfilePage();
            Assert.Throws<ArgumentException>(() => page.UpdateDisplayName(" "));
        }

        [Fact]
        public void UpdateLanguage_Valid_SetsLanguage()
        {
            var page = new UserProfilePage();
            page.UpdateLanguage("uk");
            Assert.Equal("uk", page.Language);
        }

        [Fact]
        public void UpdateLanguage_Invalid_Throws()
        {
            var page = new UserProfilePage();
            Assert.Throws<ArgumentException>(() => page.UpdateLanguage("english"));
        }

        [Fact]
        public void UpdateAvatar_Valid_SetsUrl()
        {
            var page = new UserProfilePage();
            page.UpdateAvatar("https://example.com/avatar.png");
            Assert.Equal("https://example.com/avatar.png", page.AvatarUrl);
        }

        [Fact]
        public void UpdateAvatar_Empty_Throws()
        {
            var page = new UserProfilePage();
            Assert.Throws<ArgumentException>(() => page.UpdateAvatar(""));
        }
    }
}