"""
Tests for UserProfilePage - User settings
"""
import pytest
from user_profile_page import UserProfilePage


# =============== POSITIVE TESTS ===============

def test_create_user_profile():
    """Test 365: Create user profile page"""
    profile = UserProfilePage(user_id=1)
    assert profile.user_id == 1
    assert profile.name == "Default User"
    assert profile.language == "en"

def test_change_name():
    """Test 366: Change user name"""
    profile = UserProfilePage(user_id=1)
    result = profile.change_name("John Doe")
    assert result["status"] == "success"
    assert profile.name == "John Doe"
    assert profile.is_modified is True

def test_change_language_to_spanish():
    """Test 367: Change language to Spanish"""
    profile = UserProfilePage(user_id=1)
    result = profile.change_language("es")
    assert result["status"] == "success"
    assert profile.language == "es"

def test_change_language_to_french():
    """Test 368: Change language to French"""
    profile = UserProfilePage(user_id=1)
    result = profile.change_language("fr")
    assert profile.language == "fr"

def test_change_avatar():
    """Test 369: Change user avatar"""
    profile = UserProfilePage(user_id=1)
    result = profile.change_avatar("https://example.com/avatar.jpg")
    assert result["status"] == "success"
    assert profile.avatar_url == "https://example.com/avatar.jpg"

def test_remove_avatar():
    """Test 370: Remove user avatar"""
    profile = UserProfilePage(user_id=1)
    profile.change_avatar("https://example.com/avatar.jpg")
    result = profile.remove_avatar()
    assert result["status"] == "success"
    assert profile.avatar_url is None

def test_get_profile():
    """Test 371: Get profile information"""
    profile = UserProfilePage(user_id=1)
    profile.change_name("Alice")
    profile_info = profile.get_profile()
    assert profile_info["user_id"] == 1
    assert profile_info["name"] == "Alice"
    assert profile_info["language"] == "en"

def test_save_changes():
    """Test 372: Save profile changes"""
    profile = UserProfilePage(user_id=1)
    profile.change_name("Bob")
    result = profile.save_changes()
    assert result["status"] == "success"
    assert profile.is_modified is False

def test_reset_to_defaults():
    """Test 373: Reset profile to defaults"""
    profile = UserProfilePage(user_id=1)
    profile.change_name("Alice")
    profile.change_language("es")
    result = profile.reset_to_defaults()
    assert result["status"] == "success"
    assert profile.name == "Default User"
    assert profile.language == "en"


# =============== NEGATIVE TESTS ===============

def test_create_profile_non_integer_id():
    """Test 374: Create profile with non-integer ID raises TypeError"""
    with pytest.raises(TypeError, match="User ID must be an integer"):
        UserProfilePage(user_id="1")

def test_change_name_non_string():
    """Test 375: Change name with non-string raises TypeError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(TypeError, match="Name must be a string"):
        profile.change_name(123)

def test_change_name_empty():
    """Test 376: Empty name raises ValueError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(ValueError, match="Name cannot be empty"):
        profile.change_name("   ")

def test_change_name_too_short():
    """Test 377: Name shorter than 2 characters raises ValueError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(ValueError, match="Name must be at least 2 characters"):
        profile.change_name("A")

def test_change_name_too_long():
    """Test 378: Name longer than 50 characters raises ValueError"""
    profile = UserProfilePage(user_id=1)
    long_name = "A" * 51
    with pytest.raises(ValueError, match="Name cannot exceed 50 characters"):
        profile.change_name(long_name)

def test_change_language_non_string():
    """Test 379: Change language with non-string raises TypeError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(TypeError, match="Language code must be a string"):
        profile.change_language(123)

def test_change_language_unsupported():
    """Test 380: Unsupported language raises ValueError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(ValueError, match="Unsupported language"):
        profile.change_language("ru")

def test_change_avatar_non_string():
    """Test 381: Change avatar with non-string raises TypeError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(TypeError, match="Avatar URL must be a string"):
        profile.change_avatar(123)

def test_change_avatar_empty():
    """Test 382: Empty avatar URL raises ValueError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(ValueError, match="Avatar URL cannot be empty"):
        profile.change_avatar("")

def test_change_avatar_invalid_url():
    """Test 383: Invalid avatar URL raises ValueError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(ValueError, match="Avatar URL must start with http"):
        profile.change_avatar("ftp://example.com/avatar.jpg")

def test_remove_avatar_when_none():
    """Test 384: Remove avatar when none exists raises ValueError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(ValueError, match="No avatar to remove"):
        profile.remove_avatar()

def test_save_changes_when_no_modifications():
    """Test 385: Save changes with no modifications raises ValueError"""
    profile = UserProfilePage(user_id=1)
    with pytest.raises(ValueError, match="No changes to save"):
        profile.save_changes()


# =============== EDGE CASES ===============

def test_name_whitespace_trimmed():
    """Test 386: Name whitespace is trimmed"""
    profile = UserProfilePage(user_id=1)
    profile.change_name("  Alice  ")
    assert profile.name == "Alice"

def test_avatar_url_whitespace_trimmed():
    """Test 387: Avatar URL whitespace is trimmed"""
    profile = UserProfilePage(user_id=1)
    profile.change_avatar("  https://example.com/avatar.jpg  ")
    assert profile.avatar_url == "https://example.com/avatar.jpg"

def test_is_modified_flag():
    """Test 388: is_modified flag updates correctly"""
    profile = UserProfilePage(user_id=1)
    assert profile.is_modified is False
    profile.change_name("Alice")
    assert profile.is_modified is True
    profile.save_changes()
    assert profile.is_modified is False

def test_multiple_changes_before_save():
    """Test 389: Multiple changes before saving"""
    profile = UserProfilePage(user_id=1)
    profile.change_name("Alice")
    profile.change_language("es")
    profile.change_avatar("https://example.com/avatar.jpg")
    assert profile.is_modified is True
    profile_info = profile.get_profile()
    assert profile_info["name"] == "Alice"
    assert profile_info["language"] == "es"
    assert profile_info["avatar_url"] == "https://example.com/avatar.jpg"

def test_supported_languages():
    """Test 390: All supported languages work"""
    profile = UserProfilePage(user_id=1)
    languages = ["en", "es", "fr", "de", "pt", "zh", "ja"]
    for lang in languages:
        profile.change_language(lang)
        assert profile.language == lang

def test_name_exactly_2_characters():
    """Test 391: Name with exactly 2 characters is valid"""
    profile = UserProfilePage(user_id=1)
    profile.change_name("Jo")
    assert profile.name == "Jo"

def test_name_exactly_50_characters():
    """Test 392: Name with exactly 50 characters is valid"""
    profile = UserProfilePage(user_id=1)
    name = "A" * 50
    profile.change_name(name)
    assert len(profile.name) == 50

def test_http_and_https_avatars():
    """Test 393: Both HTTP and HTTPS avatar URLs are valid"""
    profile = UserProfilePage(user_id=1)
    profile.change_avatar("http://example.com/avatar1.jpg")
    assert profile.avatar_url.startswith("http://")
    profile.change_avatar("https://example.com/avatar2.jpg")
    assert profile.avatar_url.startswith("https://")
