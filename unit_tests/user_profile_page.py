"""
UserProfilePage - User settings for name, language, and avatar
"""

class UserProfilePage:
    def __init__(self, user_id):
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer")
        self.user_id = user_id
        self.name = "Default User"
        self.language = "en"
        self.avatar_url = None
        self.is_modified = False
    
    def change_name(self, new_name):
        """Change user's display name"""
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")
        if not new_name.strip():
            raise ValueError("Name cannot be empty")
        if len(new_name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        if len(new_name.strip()) > 50:
            raise ValueError("Name cannot exceed 50 characters")
        
        self.name = new_name.strip()
        self.is_modified = True
        return {"status": "success", "message": "Name updated successfully"}
    
    def change_language(self, language_code):
        """Change user's interface language"""
        supported_languages = ["en", "es", "fr", "de", "pt", "zh", "ja"]
        
        if not isinstance(language_code, str):
            raise TypeError("Language code must be a string")
        
        if language_code not in supported_languages:
            raise ValueError(f"Unsupported language. Must be one of: {', '.join(supported_languages)}")
        
        self.language = language_code
        self.is_modified = True
        return {"status": "success", "message": f"Language changed to {language_code}"}
    
    def change_avatar(self, avatar_url):
        """Change user's profile avatar"""
        if not isinstance(avatar_url, str):
            raise TypeError("Avatar URL must be a string")
        if not avatar_url.strip():
            raise ValueError("Avatar URL cannot be empty")
        
        trimmed_url = avatar_url.strip()
        if not (trimmed_url.startswith("http://") or trimmed_url.startswith("https://")):
            raise ValueError("Avatar URL must start with http:// or https://")
        
        self.avatar_url = trimmed_url
        self.is_modified = True
        return {"status": "success", "message": "Avatar updated successfully"}
    
    def remove_avatar(self):
        """Remove user's avatar (reset to default)"""
        if self.avatar_url is None:
            raise ValueError("No avatar to remove")
        
        self.avatar_url = None
        self.is_modified = True
        return {"status": "success", "message": "Avatar removed"}
    
    def get_profile(self):
        """Get user profile information"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "language": self.language,
            "avatar_url": self.avatar_url,
            "is_modified": self.is_modified
        }
    
    def save_changes(self):
        """Save profile changes"""
        if not self.is_modified:
            raise ValueError("No changes to save")
        
        self.is_modified = False
        return {
            "status": "success",
            "message": "Profile changes saved successfully"
        }
    
    def reset_to_defaults(self):
        """Reset profile to default settings"""
        self.name = "Default User"
        self.language = "en"
        self.avatar_url = None
        self.is_modified = True
        return {"status": "success", "message": "Profile reset to defaults"}
