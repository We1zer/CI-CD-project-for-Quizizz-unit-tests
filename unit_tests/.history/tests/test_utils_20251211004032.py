import pytest
from utils import Config, Logger


# =============== CONFIG TESTS ===============

def test_config_default_language():
    """Test 90: Default language is 'en'"""
    config = Config()
    assert config.get_config()["language"] == "en"

def test_config_default_browser():
    """Test 91: Default browser is 'chrome'"""
    config = Config()
    assert config.get_config()["browser"] == "chrome"

def test_set_language_en():
    """Test 92: Set language to English"""
    config = Config()
    config.set_language("en")
    assert config.get_config()["language"] == "en"

def test_set_language_es():
    """Test 93: Set language to Spanish"""
    config = Config()
    config.set_language("es")
    assert config.get_config()["language"] == "es"

def test_set_language_fr():
    """Test 94: Set language to French"""
    config = Config()
    config.set_language("fr")
    assert config.get_config()["language"] == "fr"

def test_set_browser_chrome():
    """Test 95: Set browser to Chrome"""
    config = Config()
    config.set_browser("chrome")
    assert config.get_config()["browser"] == "chrome"

def test_set_browser_firefox():
    """Test 96: Set browser to Firefox"""
    config = Config()
    config.set_browser("firefox")
    assert config.get_config()["browser"] == "firefox"

def test_set_timeout():
    """Test 97: Set custom timeout"""
    config = Config()
    config.set_timeout(30)
    assert config.get_config()["timeout"] == 30

def test_set_headless_true():
    """Test 98: Enable headless mode"""
    config = Config()
    config.set_headless(True)
    assert config.get_config()["headless"] is True

def test_set_headless_false():
    """Test 99: Disable headless mode"""
    config = Config()
    config.set_headless(False)
    assert config.get_config()["headless"] is False

def test_get_config():
    """Test 100: Get full configuration"""
    config = Config()
    result = config.get_config()
    assert "language" in result
    assert "browser" in result
    assert "timeout" in result

def test_config_reset():
    """Test 101: Reset configuration to defaults"""
    config = Config()
    config.set_language("fr")
    config.reset()
    assert config.get_config()["language"] == "en"


# =============== LOGGER TESTS ===============

def test_log_info():
    """Test 102: Log info message"""
    logger = Logger()
    result = logger.log("Test message", "info")
    assert "info" in result.lower()

def test_log_warning():
    """Test 103: Log warning message"""
    logger = Logger()
    result = logger.log("Warning", "warning")
    assert "warning" in result.lower()

def test_log_error():
    """Test 104: Log error message"""
    logger = Logger()
    result = logger.log("Error", "error")
    assert "error" in result.lower()

def test_log_debug():
    """Test 105: Log debug message"""
    logger = Logger()
    result = logger.log("Debug", "debug")
    assert "debug" in result.lower()

def test_log_default_level():
    """Test 106: Default log level is info"""
    logger = Logger()
    result = logger.log("Test")
    assert "info" in result.lower()


# =============== UTILITY FUNCTION TESTS ===============

def test_validate_url_http():
    """Test 107: Validate HTTP URL"""
    from utils import validate_url
    assert validate_url("http://quizizz.com") is True

def test_validate_url_https():
    """Test 108: Validate HTTPS URL"""
    from utils import validate_url
    assert validate_url("https://quizizz.com") is True

def test_format_time_seconds():
    """Test 109: Format time in seconds"""
    from utils import format_time
    result = format_time(45)
    assert "45" in result
    assert "sec" in result

def test_format_time_minutes():
    """Test 110: Format time in minutes"""
    from utils import format_time
    result = format_time(120)
    assert "2" in result
    assert "min" in result

def test_format_score_percentage():
    """Test 111: Format score as percentage"""
    from utils import format_score
    result = format_score(80, 100)
    assert "80" in result
    assert "%" in result

def test_parse_json_valid():
    """Test 112: Parse valid JSON string"""
    from utils import parse_json
    result = parse_json('{"key": "value"}')
    assert result["key"] == "value"


# =============== NEGATIVE TESTS ===============

def test_set_language_invalid():
    """Test 113: Set invalid language raises error"""
    config = Config()
    with pytest.raises(ValueError, match="Unsupported language"):
        config.set_language("invalid_lang")

def test_set_browser_invalid():
    """Test 114: Set invalid browser raises error"""
    config = Config()
    with pytest.raises(ValueError, match="Unsupported browser"):
        config.set_browser("invalid_browser")

def test_set_timeout_zero():
    """Test 115: Set timeout to 0 raises error"""
    config = Config()
    with pytest.raises(ValueError, match="Timeout must be positive"):
        config.set_timeout(0)

def test_set_timeout_negative():
    """Test 116: Set negative timeout raises error"""
    config = Config()
    with pytest.raises(ValueError, match="Timeout must be positive"):
        config.set_timeout(-10)

def test_set_headless_non_boolean():
    """Test 117: Set headless to non-boolean raises error"""
    config = Config()
    with pytest.raises(TypeError, match="Headless must be boolean"):
        config.set_headless("yes")

def test_log_non_string():
    """Test 118: Log non-string message raises error"""
    logger = Logger()
    with pytest.raises(TypeError, match="Message must be a string"):
        logger.log(12345)

def test_log_invalid_level():
    """Test 119: Log with invalid level raises error"""
    logger = Logger()
    with pytest.raises(ValueError, match="Invalid log level"):
        logger.log("Test", "invalid_level")

def test_validate_url_non_string():
    """Test 120: Validate non-string URL raises error"""
    from utils import validate_url
    with pytest.raises(TypeError, match="URL must be a string"):
        validate_url(12345)

def test_validate_url_invalid_protocol():
    """Test 121: Validate URL with invalid protocol"""
    from utils import validate_url
    assert validate_url("ftp://example.com") is False

def test_validate_url_no_protocol():
    """Test 122: Validate URL without protocol"""
    from utils import validate_url
    assert validate_url("quizizz.com") is False

def test_format_score_invalid_total():
    """Test 123: Format score with 0 total raises error"""
    from utils import format_score
    with pytest.raises(ValueError, match="Total must be positive"):
        format_score(50, 0)

def test_format_time_negative():
    """Test 124: Format negative time raises error"""
    from utils import format_time
    with pytest.raises(ValueError, match="Time cannot be negative"):
        format_time(-10)

def test_parse_json_invalid():
    """Test 125: Parse invalid JSON raises error"""
    from utils import parse_json
    with pytest.raises(ValueError, match="Invalid JSON"):
        parse_json("not json")


# =============== EDGE CASE TESTS ===============

def test_format_time_zero():
    """Test 126: Format 0 seconds"""
    from utils import format_time
    result = format_time(0)
    assert "0" in result

def test_format_score_perfect():
    """Test 127: Format perfect score (100%)"""
    from utils import format_score
    result = format_score(100, 100)
    assert "100" in result
