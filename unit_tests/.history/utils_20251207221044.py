
class Config:
    language = "ua"
    browser = "chrome"
    timeout = 30
    headless = False

    @staticmethod
    def set_language(lang):
        if lang not in ("ua", "ru", "en"):
            raise ValueError("Invalid language")
        Config.language = lang

    @staticmethod
    def set_browser(br):
        if br not in ("chrome", "firefox"):
            raise ValueError("Invalid browser")
        Config.browser = br
    
    @staticmethod
    def set_timeout(seconds):
        if seconds <= 0:
            raise ValueError("Timeout must be positive")
        Config.timeout = seconds
    
    @staticmethod
    def set_headless(mode):
        if not isinstance(mode, bool):
            raise TypeError("Headless mode must be boolean")
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
        Config.language = "ua"
        Config.browser = "chrome"
        Config.timeout = 30
        Config.headless = False

def log(message, level="INFO"):
    if not isinstance(message, str):
        raise TypeError("Message must be string")
    if level not in ("INFO", "WARNING", "ERROR", "DEBUG"):
        raise ValueError("Invalid log level")
    return f"[{level}] LOG: {message}"

def validate_url(url):
    if not isinstance(url, str):
        raise TypeError("URL must be string")
    if not url.startswith(("http://", "https://")):
        raise ValueError("Invalid URL format")
    return True

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
