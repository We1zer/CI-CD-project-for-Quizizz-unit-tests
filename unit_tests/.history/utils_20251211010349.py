
class Config:
    """Configuration for Quizizz testing framework"""
    language = "en"
    browser = "chrome"
    timeout = 30
    headless = False

    @staticmethod
    def set_language(lang):
        if lang not in ("en", "es", "fr"):
            raise ValueError("Unsupported language")
        Config.language = lang

    @staticmethod
    def set_browser(br):
        if br not in ("chrome", "firefox"):
            raise ValueError("Unsupported browser")
        Config.browser = br
    
    @staticmethod
    def set_timeout(seconds):
        if seconds <= 0:
            raise ValueError("Timeout must be positive")
        Config.timeout = seconds
    
    @staticmethod
    def set_headless(mode):
        if not isinstance(mode, bool):
            raise TypeError("Headless must be boolean")
        Config.headless = mode
    
    @staticmethod
    def get_config():
        return {
            "language": Config.language,
            "browser": Config.browser,
            "timeout": Config.timeout,
            "headless": Config.headless
        }
    
    @staticmethod
    def reset():
        Config.language = "en"
        Config.browser = "chrome"
        Config.timeout = 30
        Config.headless = False


class Logger:
    """Logger for Quizizz test framework"""
    
    def log(self, message, level="info"):
        if not isinstance(message, str):
            raise TypeError("Message must be a string")
        if level not in ("info", "warning", "error", "debug"):
            raise ValueError("Invalid log level")
        return f"[{level.upper()}] {message}"


def validate_url(url):
    """Validate URL format"""
    if not isinstance(url, str):
        raise TypeError("URL must be a string")
    return url.startswith("http://") or url.startswith("https://")


def format_time(seconds):
    """Format time in seconds to readable string"""
    if seconds < 0:
        raise ValueError("Time cannot be negative")
    if seconds < 60:
        return f"{seconds} sec"
    minutes = seconds // 60
    return f"{minutes} min"


def format_score(score, total):
    """Format score as percentage"""
    if total <= 0:
        raise ValueError("Total must be positive")
    percentage = (score / total) * 100
    return f"{percentage:.0f}%"


def parse_json(json_string):
    """Parse JSON string"""
    import json
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")
    if level not in ("INFO", "WARNING", "ERROR", "DEBUG"):
        raise ValueError("Invalid log level")
    return f"[{level}] LOG: {message}"

def validate_url(url):
    """Validate URL format"""
    if not isinstance(url, str):
        raise TypeError("URL must be a string")
    return url.startswith("http://") or url.startswith("https://")

def parse_json_config(json_str):
    import json
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

def format_price(price, currency="UAH"):
    if not isinstance(price, (int, float)):
        raise TypeError("Price must be numeric")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return f"{price:.2f} {currency}"
