"""
Приклад тесту з повною інтеграцією Allure звітності
Демонструє використання всіх Allure features
"""

import pytest
import allure
from datetime import datetime


@allure.epic('Quizizz Test Framework')
@allure.feature('Example Tests')
class TestAllureIntegration:
    """Приклади використання Allure в тестах"""
    
    @allure.story('Basic Test Example')
    @allure.title('Простий тест з Allure annotations')
    @allure.description("""
    Цей тест демонструє базове використання Allure.
    Він включає:
    - Title та description
    - Severity level
    - Steps
    - Attachments
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag('example', 'smoke')
    @allure.label('owner', 'Test Team')
    def test_basic_allure_example(self):
        """Базовий приклад з Allure"""
        
        with allure.step('Крок 1: Підготовка даних'):
            test_data = {'name': 'Test Quiz', 'questions': 10}
            allure.attach(
                str(test_data),
                name='Test Data',
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step('Крок 2: Виконання операції'):
            result = test_data['questions'] * 2
            allure.attach(
                f"Result: {result}",
                name='Operation Result',
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step('Крок 3: Перевірка результату'):
            assert result == 20, f"Expected 20, got {result}"
        
        allure.dynamic.description_html("""
        <h3>Test Details</h3>
        <ul>
            <li>✅ Data preparation completed</li>
            <li>✅ Operation executed successfully</li>
            <li>✅ Result verified</li>
        </ul>
        """)
    
    @allure.story('Parametrized Test Example')
    @allure.title('Test with parameters: {subject} - {expected_count}')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('subject,expected_count', [
        ('Math', 15),
        ('Science', 12),
        ('History', 8)
    ])
    def test_parametrized_with_allure(self, subject, expected_count):
        """Параметризований тест з Allure"""
        
        allure.dynamic.parameter('Subject', subject)
        allure.dynamic.parameter('Expected Count', expected_count)
        
        with allure.step(f'Search quizzes for subject: {subject}'):
            # Симуляція пошуку
            found_count = expected_count  # Mock result
        
        with allure.step('Verify search results'):
            assert found_count == expected_count, \
                f"Expected {expected_count} quizzes, found {found_count}"
    
    @allure.story('Performance Test Example')
    @allure.title('Test performance measurement')
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag('performance')
    def test_performance_with_allure(self, performance_tracker):
        """Тест з вимірюванням продуктивності"""
        
        performance_tracker.start()
        
        with allure.step('Execute time-consuming operation'):
            # Симуляція операції
            import time
            time.sleep(0.1)
            result = sum(range(10000))
        
        duration = performance_tracker.stop()
        
        with allure.step('Check performance threshold'):
            threshold = 1.0  # 1 second
            assert duration < threshold, \
                f"Operation took {duration}s, threshold is {threshold}s"
    
    @allure.story('Test with Attachments')
    @allure.title('Test demonstrating different attachment types')
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_allure_attachments(self):
        """Демонстрація різних типів вкладень"""
        
        with allure.step('Attach text'):
            allure.attach(
                'This is a text attachment',
                name='Text Example',
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step('Attach JSON'):
            import json
            data = {
                'quiz_id': '123',
                'title': 'Math Quiz',
                'questions': 15
            }
            allure.attach(
                json.dumps(data, indent=2),
                name='Quiz Data',
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step('Attach CSV'):
            csv_data = "Name,Score,Time\nStudent1,95,120\nStudent2,87,115"
            allure.attach(
                csv_data,
                name='Results CSV',
                attachment_type=allure.attachment_type.CSV
            )
        
        with allure.step('Attach HTML'):
            html_content = """
            <div style="padding: 10px; background: #f0f0f0;">
                <h3>Test Results</h3>
                <p>All checks passed ✅</p>
            </div>
            """
            allure.attach(
                html_content,
                name='HTML Report',
                attachment_type=allure.attachment_type.HTML
            )
    
    @allure.story('Test with Links')
    @allure.title('Test with external references')
    @allure.link('https://github.com/your-repo', name='GitHub Repository')
    @allure.issue('JIRA-123', 'Related Jira Issue')
    @allure.testcase('TC-456', 'Test Case in TMS')
    def test_with_links(self):
        """Тест з посиланнями на зовнішні ресурси"""
        
        with allure.step('Add dynamic link'):
            allure.dynamic.link('https://docs.pytest.org', name='Pytest Docs')
        
        assert True, "Test with links"
    
    @allure.story('Conditional Test Example')
    @allure.title('Test with conditional execution')
    @pytest.mark.skipif(
        datetime.now().weekday() == 6,  # Skip on Sunday
        reason='Not running on Sundays'
    )
    def test_conditional_execution(self):
        """Тест з умовним виконанням"""
        
        with allure.step('Check execution day'):
            current_day = datetime.now().strftime('%A')
            allure.attach(
                f"Test executed on: {current_day}",
                name='Execution Day',
                attachment_type=allure.attachment_type.TEXT
            )
        
        assert True


@allure.epic('Quizizz Test Framework')
@allure.feature('BDD Integration Example')
class TestBDDStyleWithAllure:
    """Приклади BDD-style тестів з Allure"""
    
    @allure.story('Given-When-Then Pattern')
    @allure.title('BDD style test with Allure')
    @allure.severity(allure.severity_level.NORMAL)
    def test_bdd_style(self):
        """BDD-style тест з Allure steps"""
        
        # GIVEN
        with allure.step('GIVEN user is on quiz search page'):
            page_loaded = True
            assert page_loaded
        
        # WHEN
        with allure.step('WHEN user searches for "Math"'):
            search_term = "Math"
            results = ['Math Quiz 1', 'Math Quiz 2', 'Math Quiz 3']
            allure.attach(
                f"Search term: {search_term}\nResults: {results}",
                name='Search Results',
                attachment_type=allure.attachment_type.TEXT
            )
        
        # THEN
        with allure.step('THEN relevant results are displayed'):
            assert len(results) > 0
            assert all('Math' in r for r in results)


@allure.epic('Quizizz Test Framework')
@allure.feature('Failure Handling')
class TestFailureExamples:
    """Приклади обробки помилок з Allure"""
    
    @allure.story('Expected Failure')
    @allure.title('Test expected to fail (xfail)')
    @pytest.mark.xfail(reason='Known bug: JIRA-789')
    def test_expected_failure(self):
        """Тест, який очікується невдалим"""
        
        with allure.step('Perform operation'):
            result = 1 + 1
        
        with allure.step('Check result (will fail)'):
            assert result == 3, "This is expected to fail"
    
    @allure.story('Conditional Skip')
    @allure.title('Test that might be skipped')
    @pytest.mark.skip(reason='Feature not implemented yet')
    def test_conditional_skip(self):
        """Тест, який пропускається"""
        
        with allure.step('This step will not execute'):
            assert False


# Приклад використання в CLI:
"""
# Запуск всіх прикладів з Allure
pytest tests/test_allure_examples.py --alluredir=allure-results -v

# Генерація звіту
allure generate allure-results -o allure-report --clean

# Відкриття звіту
allure open allure-report

# Запуск з фільтрацією за severity
pytest tests/test_allure_examples.py --allure-severities=critical,normal
"""
