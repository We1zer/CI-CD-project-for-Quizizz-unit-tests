import pytest
from utils import Config, log, validate_url, parse_json_config, format_price


# ============== CONFIG TESTS ==============

def test_config_default_language():
    """Test 83: Config has default language"""
    Config.reset()
    assert Config.language == "ua"


def test_config_default_browser():
    """Test 84: Config has default browser"""
    Config.reset()
    assert Config.browser == "chrome"


def test_set_language_ua():
    """Test 85: Set language to Ukrainian"""
    Config.set_language("ua")
    assert Config.language == "ua"


def test_set_language_ru():
    """Test 86: Set language to Russian"""
    Config.set_language("ru")
    assert Config.language == "ru"


def test_set_language_en():
    """Test 87: Set language to English"""
    Config.set_language("en")
    assert Config.language == "en"


def test_set_browser_chrome():
    """Test 88: Set browser to Chrome"""
    Config.set_browser("chrome")
    assert Config.browser == "chrome"


def test_set_browser_firefox():
    """Test 89: Set browser to Firefox"""
    Config.set_browser("firefox")
    assert Config.browser == "firefox"


def test_set_timeout():
    """Test 90: Set timeout value"""
    Config.set_timeout(60)
    assert Config.timeout == 60


def test_set_headless_true():
    """Test 91: Set headless mode to True"""
    Config.set_headless(True)
    assert Config.headless is True


def test_set_headless_false():
    """Test 92: Set headless mode to False"""
    Config.set_headless(False)
    assert Config.headless is False


def test_get_config():
    """Test 93: Get complete config dictionary"""
    Config.reset()
    config = Config.get_config()
    assert "language" in config
    assert "browser" in config
    assert "timeout" in config
    assert "headless" in config


def test_config_reset():
    """Test 94: Reset config to defaults"""
    Config.set_language("en")
    Config.set_browser("firefox")
    Config.reset()
    assert Config.language == "ua"
    assert Config.browser == "chrome"


# ============== LOG TESTS ==============

def test_log_info():
    """Test 95: Log info message"""
    result = log("Test message", "INFO")
    assert "[INFO]" in result
    assert "Test message" in result


def test_log_warning():
    """Test 96: Log warning message"""
    result = log("Warning", "WARNING")
    assert "[WARNING]" in result


def test_log_error():
    """Test 97: Log error message"""
    result = log("Error occurred", "ERROR")
    assert "[ERROR]" in result


def test_log_debug():
    """Test 98: Log debug message"""
    result = log("Debug info", "DEBUG")
    assert "[DEBUG]" in result


def test_log_default_level():
    """Test 99: Log with default INFO level"""
    result = log("Message")
    assert "[INFO]" in result


# ============== VALIDATION TESTS ==============

def test_validate_url_http():
    """Test 100: Validate HTTP URL"""
    assert validate_url("http://example.com") is True


def test_validate_url_https():
    """Test 101: Validate HTTPS URL"""
    assert validate_url("https://rozetka.com.ua") is True


def test_format_price_integer():
    """Test 102: Format integer price"""
    result = format_price(100)
    assert result == "100.00 UAH"


def test_format_price_float():
    """Test 103: Format float price"""
    result = format_price(99.99)
    assert result == "99.99 UAH"


def test_format_price_custom_currency():
    """Test 104: Format price with custom currency"""
    result = format_price(50, "USD")
    assert result == "50.00 USD"


def test_parse_json_valid():
    """Test 105: Parse valid JSON string"""
    result = parse_json_config('{"key": "value"}')
    assert result["key"] == "value"


# ============== NEGATIVE TESTS ==============

def test_set_language_invalid():
    """Test 106: Set invalid language raises ValueError"""
    with pytest.raises(ValueError, match="Invalid language"):
        Config.set_language("de")


def test_set_browser_invalid():
    """Test 107: Set invalid browser raises ValueError"""
    with pytest.raises(ValueError, match="Invalid browser"):
        Config.set_browser("safari")


def test_set_timeout_zero():
    """Test 108: Set timeout to zero raises ValueError"""
    with pytest.raises(ValueError, match="Timeout must be positive"):
        Config.set_timeout(0)


def test_set_timeout_negative():
    """Test 109: Set negative timeout raises ValueError"""
    with pytest.raises(ValueError, match="Timeout must be positive"):
        Config.set_timeout(-10)


def test_set_headless_non_boolean():
    """Test 110: Set headless to non-boolean raises TypeError"""
    with pytest.raises(TypeError, match="Headless mode must be boolean"):
        Config.set_headless("true")


def test_log_non_string():
    """Test 111: Log non-string message raises TypeError"""
    with pytest.raises(TypeError, match="Message must be string"):
        log(123)


def test_log_invalid_level():
    """Test 112: Log with invalid level raises ValueError"""
    with pytest.raises(ValueError, match="Invalid log level"):
        log("message", "INVALID")


def test_validate_url_non_string():
    """Test 113: Validate non-string URL raises TypeError"""
    with pytest.raises(TypeError, match="URL must be string"):
        validate_url(123)


def test_validate_url_invalid_protocol():
    """Test 114: Validate URL without http/https raises ValueError"""
    with pytest.raises(ValueError, match="Invalid URL format"):
        validate_url("ftp://example.com")


def test_validate_url_no_protocol():
    """Test 115: Validate URL without protocol raises ValueError"""
    with pytest.raises(ValueError, match="Invalid URL format"):
        validate_url("example.com")


def test_format_price_non_numeric():
    """Test 116: Format non-numeric price raises TypeError"""
    with pytest.raises(TypeError, match="Price must be numeric"):
        format_price("100")


def test_format_price_negative():
    """Test 117: Format negative price raises ValueError"""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        format_price(-50)


def test_parse_json_invalid():
    """Test 118: Parse invalid JSON raises ValueError"""
    with pytest.raises(ValueError, match="Invalid JSON"):
        parse_json_config("invalid json")
