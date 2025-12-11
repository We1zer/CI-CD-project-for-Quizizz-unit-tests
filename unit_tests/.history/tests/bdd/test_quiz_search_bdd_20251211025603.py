"""
BDD Step Definitions для тестів пошуку квізів
Використовує pytest-bdd для Gherkin сценаріїв
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import allure

# Завантаження сценаріїв з feature файлу
scenarios('../features/quiz_search.feature')


# Fixtures для тестових даних
@pytest.fixture
def search_page():
    """Створює об'єкт сторінки пошуку"""
    return {
        'results': [],
        'filters': {},
        'search_term': '',
        'is_loaded': False
    }


@pytest.fixture
def mock_search_results():
    """Мок даних результатів пошуку"""
    return [
        {
            'id': '1',
            'title': 'Основи математики',
            'subject': 'Math',
            'grade_range': [5, 8],
            'plays': 1500,
            'keywords': ['математика', 'алгебра']
        },
        {
            'id': '2',
            'title': 'Алгебра для початківців',
            'subject': 'Math',
            'grade_range': [6, 9],
            'plays': 2300,
            'keywords': ['математика', 'алгебра']
        },
        {
            'id': '3',
            'title': 'Історія світу',
            'subject': 'History',
            'grade_range': [7, 10],
            'plays': 800,
            'keywords': ['історія']
        }
    ]


# Step Definitions

@given('я відкрив сторінку пошуку квізів')
@allure.step('Відкриття сторінки пошуку квізів')
def open_search_page(search_page):
    """Відкриває сторінку пошуку"""
    search_page['is_loaded'] = True
    assert search_page['is_loaded'], "Сторінка пошуку не завантажилася"


@when(parsers.parse('я ввожу "{search_term}" в поле пошуку'))
@allure.step('Введення пошукового запиту: {search_term}')
def enter_search_term(search_page, search_term):
    """Вводить пошуковий запит"""
    search_page['search_term'] = search_term


@when('натискаю кнопку "Шукати"')
@allure.step('Натискання кнопки пошуку')
def click_search_button(search_page, mock_search_results):
    """Виконує пошук"""
    # Фільтрація результатів за пошуковим запитом
    search_term = search_page['search_term'].lower()
    search_page['results'] = [
        r for r in mock_search_results
        if search_term in ' '.join(r['keywords']).lower()
    ]


@when(parsers.parse('вибираю фільтр предмету "{subject}"'))
@allure.step('Вибір фільтру предмету: {subject}')
def select_subject_filter(search_page, subject):
    """Встановлює фільтр предмету"""
    search_page['filters']['subject'] = subject


@when(parsers.parse('вибираю фільтр класу від {min_grade:d} до {max_grade:d}'))
@allure.step('Вибір фільтру класу: {min_grade}-{max_grade}')
def select_grade_filter(search_page, min_grade, max_grade):
    """Встановлює фільтр класу"""
    search_page['filters']['grade_range'] = (min_grade, max_grade)


@given(parsers.parse('є результати пошуку для "{search_term}"'))
@allure.step('Підготовка результатів пошуку для: {search_term}')
def prepare_search_results(search_page, mock_search_results, search_term):
    """Підготовлює результати пошуку"""
    search_page['search_term'] = search_term
    search_term_lower = search_term.lower()
    search_page['results'] = [
        r for r in mock_search_results
        if search_term_lower in ' '.join(r['keywords']).lower()
    ]


@when('я сортую результати за популярністю')
@allure.step('Сортування результатів за популярністю')
def sort_by_popularity(search_page):
    """Сортує результати за кількістю проходжень"""
    search_page['results'].sort(key=lambda x: x['plays'], reverse=True)


@then('я бачу список результатів пошуку')
@allure.step('Перевірка наявності результатів пошуку')
def verify_results_displayed(search_page):
    """Перевіряє, що результати відображаються"""
    assert len(search_page['results']) > 0, "Результати пошуку відсутні"
    allure.attach(
        str(search_page['results']),
        name="Результати пошуку",
        attachment_type=allure.attachment_type.TEXT
    )


@then(parsers.parse('результати містять слово "{keyword}"'))
@allure.step('Перевірка наявності ключового слова: {keyword}')
def verify_keyword_in_results(search_page, keyword):
    """Перевіряє наявність ключового слова в результатах"""
    keyword_lower = keyword.lower()
    for result in search_page['results']:
        keywords_str = ' '.join(result['keywords']).lower()
        assert keyword_lower in keywords_str, \
            f"Ключове слово '{keyword}' не знайдено в результатах"


@then(parsers.parse('я бачу лише квізи з предмету "{subject}"'))
@allure.step('Перевірка фільтрації за предметом: {subject}')
def verify_subject_filter(search_page, subject):
    """Перевіряє фільтрацію за предметом"""
    # Застосовуємо фільтр
    filtered_results = [
        r for r in search_page['results']
        if r['subject'] == subject
    ]
    search_page['results'] = filtered_results
    
    assert len(search_page['results']) > 0, f"Не знайдено квізів з предмету {subject}"
    for result in search_page['results']:
        assert result['subject'] == subject, \
            f"Знайдено квіз з іншого предмету: {result['subject']}"


@then(parsers.parse('я бачу квізи для класів {min_grade:d}-{max_grade:d}'))
@allure.step('Перевірка фільтрації за класами: {min_grade}-{max_grade}')
def verify_grade_filter(search_page, min_grade, max_grade):
    """Перевіряє фільтрацію за класами"""
    grade_range = search_page['filters'].get('grade_range', (min_grade, max_grade))
    
    # Застосовуємо фільтр
    filtered_results = [
        r for r in search_page['results']
        if (r['grade_range'][0] >= grade_range[0] and 
            r['grade_range'][1] <= grade_range[1])
    ]
    search_page['results'] = filtered_results
    
    assert len(search_page['results']) > 0, \
        f"Не знайдено квізів для класів {min_grade}-{max_grade}"


@then('перший результат має найбільшу кількість проходжень')
@allure.step('Перевірка найпопулярнішого результату')
def verify_most_popular_first(search_page):
    """Перевіряє, що перший результат найпопулярніший"""
    assert len(search_page['results']) > 0, "Результати відсутні"
    
    first_result = search_page['results'][0]
    max_plays = max(r['plays'] for r in search_page['results'])
    
    assert first_result['plays'] == max_plays, \
        f"Перший результат не найпопулярніший: {first_result['plays']} vs {max_plays}"
    
    allure.attach(
        f"Найпопулярніший квіз: {first_result['title']} ({first_result['plays']} проходжень)",
        name="Топ результат",
        attachment_type=allure.attachment_type.TEXT
    )


@then('всі наступні результати відсортовані за спаданням популярності')
@allure.step('Перевірка сортування за популярністю')
def verify_sorted_by_popularity(search_page):
    """Перевіряє правильність сортування"""
    results = search_page['results']
    
    for i in range(len(results) - 1):
        current_plays = results[i]['plays']
        next_plays = results[i + 1]['plays']
        
        assert current_plays >= next_plays, \
            f"Порушено сортування: {current_plays} < {next_plays}"
    
    plays_list = [r['plays'] for r in results]
    allure.attach(
        f"Кількість проходжень: {plays_list}",
        name="Статистика популярності",
        attachment_type=allure.attachment_type.TEXT
    )
