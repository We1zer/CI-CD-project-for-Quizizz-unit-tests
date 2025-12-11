"""
Pytest Configuration File
Містить fixtures та конфігурацію для всіх тестів
"""

import pytest
import json
import os
from pathlib import Path
import allure
from datetime import datetime


# ========================================
# Pytest Hooks
# ========================================

def pytest_configure(config):
    """Конфігурація pytest при запуску"""
    # Додавання custom markers
    config.addinivalue_line("markers", "smoke: швидкі smoke тести")
    config.addinivalue_line("markers", "regression: регресійні тести")
    config.addinivalue_line("markers", "integration: інтеграційні тести")
    
    # Створення директорій для звітів
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    allure_dir = Path("allure-results")
    allure_dir.mkdir(exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Модифікація зібраних тестів"""
    for item in items:
        # Автоматично додати marker 'unit' для всіх тестів не в bdd/
        if "bdd" not in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Додати Allure labels
        if hasattr(item, 'module'):
            module_name = item.module.__name__
            allure.dynamic.feature(module_name.split('.')[-1])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Створення звіту про тест"""
    outcome = yield
    rep = outcome.get_result()
    
    # Додавання скріншоту для failed тестів (для майбутніх UI тестів)
    if rep.when == "call" and rep.failed:
        allure.attach(
            f"Test failed: {item.name}\n"
            f"Duration: {call.stop - call.start:.2f}s\n"
            f"Exception: {call.excinfo}",
            name="Failure Details",
            attachment_type=allure.attachment_type.TEXT
        )


# ========================================
# Session Fixtures
# ========================================

@pytest.fixture(scope="session")
def test_config():
    """Конфігурація тестів для всієї сесії"""
    return {
        'environment': os.getenv('ENVIRONMENT', 'local'),
        'max_workers': int(os.getenv('MAX_WORKERS', '4')),
        'timeout': int(os.getenv('DEFAULT_TIMEOUT', '30')),
        'reports_dir': Path('reports'),
        'mock_data_dir': Path('mock_data')
    }


@pytest.fixture(scope="session")
def mock_data_dir(test_config):
    """Шлях до директорії з mock даними"""
    return test_config['mock_data_dir']


@pytest.fixture(scope="session")
def reports_dir(test_config):
    """Шлях до директорії зі звітами"""
    return test_config['reports_dir']


# ========================================
# Function Fixtures
# ========================================

@pytest.fixture
def timestamp():
    """Поточний timestamp для тестів"""
    return datetime.now().isoformat()


@pytest.fixture
def test_metadata(request):
    """Метадані про поточний тест"""
    return {
        'name': request.node.name,
        'module': request.node.module.__name__,
        'markers': [m.name for m in request.node.iter_markers()],
        'timestamp': datetime.now().isoformat()
    }


# ========================================
# Mock Data Fixtures
# ========================================

@pytest.fixture
def load_mock_json():
    """Функція для завантаження mock JSON даних"""
    def _load(filename):
        mock_data_path = Path('mock_data') / filename
        if not mock_data_path.exists():
            pytest.skip(f"Mock data file not found: {filename}")
        
        with open(mock_data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return _load


@pytest.fixture
def search_results_data(load_mock_json):
    """Mock дані результатів пошуку"""
    return load_mock_json('search_results.json')


@pytest.fixture
def category_tree_data(load_mock_json):
    """Mock дані дерева категорій"""
    return load_mock_json('category_tree.json')


# ========================================
# Allure Fixtures
# ========================================

@pytest.fixture(autouse=True)
def allure_environment_info(request):
    """Додає інформацію про середовище до Allure звіту"""
    allure.dynamic.parameter("Test Environment", os.getenv('ENVIRONMENT', 'local'))
    allure.dynamic.parameter("Python Version", os.sys.version.split()[0])
    allure.dynamic.parameter("Test File", request.node.fspath.basename)


@pytest.fixture
def allure_step():
    """Helper для створення Allure steps"""
    def _step(name):
        return allure.step(name)
    return _step


# ========================================
# Performance Fixtures
# ========================================

@pytest.fixture
def performance_tracker():
    """Трекер для вимірювання продуктивності тестів"""
    class PerformanceTracker:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = datetime.now()
        
        def stop(self):
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            allure.attach(
                f"Execution time: {duration:.2f}s",
                name="Performance",
                attachment_type=allure.attachment_type.TEXT
            )
            return duration
    
    return PerformanceTracker()


# ========================================
# Cleanup Fixtures
# ========================================

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Очищення після кожного тесту"""
    yield
    # Тут можна додати cleanup логіку
    pass


@pytest.fixture(scope="session", autouse=True)
def cleanup_session():
    """Очищення після всієї тестової сесії"""
    yield
    # Cleanup після всіх тестів
    print("\n✅ Test session completed")


# ========================================
# Custom Markers
# ========================================

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Кастомний summary у кінці виконання тестів"""
    print("\n" + "="*60)
    print("📊 Test Execution Summary")
    print("="*60)
    
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    total = passed + failed + skipped
    
    print(f"Total Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped: {skipped}")
    
    if total > 0:
        success_rate = (passed / total) * 100
        print(f"Success Rate: {success_rate:.2f}%")
    
    print("="*60)
