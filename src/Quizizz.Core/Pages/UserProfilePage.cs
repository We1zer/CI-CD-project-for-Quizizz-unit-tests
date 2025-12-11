using System;

namespace Quizizz.Core.Pages
{
    /// <summary>
    /// Represents the user's profile settings.  Allows updating the name,
    /// language and avatar.  Throws exceptions on invalid input.
    /// </summary>
    public class UserProfilePage
    {
        public string DisplayName { get; private set; } = "Anonymous";
        public string Language { get; private set; } = "en";
        public string AvatarUrl { get; private set; } = string.Empty;

        public void UpdateDisplayName(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
            {
                throw new ArgumentException("Display name cannot be empty");
            }
            DisplayName = name;
        }

        public void UpdateLanguage(string languageCode)
        {
            if (string.IsNullOrWhiteSpace(languageCode) || languageCode.Length != 2)
            {
                throw new ArgumentException("Language code must be a two‑letter ISO 639‑1 code");
            }
            Language = languageCode.ToLowerInvariant();
        }

        public void UpdateAvatar(string avatarUrl)
        {
            if (string.IsNullOrWhiteSpace(avatarUrl))
            {
                throw new ArgumentException("Avatar URL cannot be empty");
            }
            AvatarUrl = avatarUrl;
        }
    }
}