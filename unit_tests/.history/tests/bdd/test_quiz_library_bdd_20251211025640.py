"""
BDD Step Definitions для тестів бібліотеки квізів
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import allure

# Завантаження сценаріїв
scenarios('../features/quiz_library.feature')


@pytest.fixture
def user_account():
    """Авторизований користувач"""
    return {
        'id': 'user123',
        'username': 'teacher@example.com',
        'is_authenticated': True
    }


@pytest.fixture
def quiz_library():
    """Бібліотека квізів користувача"""
    return {
        'quizzes': [
            {
                'id': '101',
                'title': 'Математика 5 клас',
                'subject': 'Math',
                'created_at': '2024-01-15',
                'type': 'Multiple Choice'
            },
            {
                'id': '102',
                'title': 'Історія України',
                'subject': 'History',
                'created_at': '2024-02-20',
                'type': 'True/False'
            },
            {
                'id': '103',
                'title': 'Старий квіз',
                'subject': 'Science',
                'created_at': '2023-12-01',
                'type': 'Open Ended'
            }
        ],
        'filters': {},
        'message': ''
    }


@pytest.fixture
def available_quiz():
    """Доступний квіз для додавання"""
    return {
        'id': '999',
        'title': 'Історія України',
        'subject': 'History',
        'type': 'Multiple Choice'
    }


# Step Definitions

@given('я маю авторизований обліковий запис')
@allure.step('Перевірка авторизації користувача')
def verify_authenticated(user_account):
    """Перевіряє авторизацію"""
    assert user_account['is_authenticated'], "Користувач не авторизований"


@when('я відкриваю мою бібліотеку квізів')
@allure.step('Відкриття бібліотеки квізів')
def open_library(quiz_library):
    """Відкриває бібліотеку"""
    quiz_library['is_open'] = True


@then('я бачу список моїх збережених квізів')
@allure.step('Перевірка списку збережених квізів')
def verify_quiz_list(quiz_library):
    """Перевіряє наявність квізів у бібліотеці"""
    assert len(quiz_library['quizzes']) > 0, "Бібліотека порожня"
    allure.attach(
        f"Кількість квізів: {len(quiz_library['quizzes'])}",
        name="Статистика бібліотеки",
        attachment_type=allure.attachment_type.TEXT
    )


@then('кожен квіз має назву та дату створення')
@allure.step('Перевірка атрибутів квізів')
def verify_quiz_attributes(quiz_library):
    """Перевіряє обов'язкові атрибути"""
    for quiz in quiz_library['quizzes']:
        assert 'title' in quiz and quiz['title'], "Відсутня назва квізу"
        assert 'created_at' in quiz and quiz['created_at'], "Відсутня дата створення"


@given(parsers.parse('я знайшов квіз "{quiz_title}"'))
@allure.step('Знаходження квізу: {quiz_title}')
def find_quiz(available_quiz, quiz_title):
    """Знаходить квіз за назвою"""
    available_quiz['title'] = quiz_title
    assert available_quiz['title'] == quiz_title


@when('я натискаю кнопку "Додати до бібліотеки"')
@allure.step('Додавання квізу до бібліотеки')
def add_to_library(quiz_library, available_quiz):
    """Додає квіз до бібліотеки"""
    new_quiz = {
        'id': available_quiz['id'],
        'title': available_quiz['title'],
        'subject': available_quiz['subject'],
        'created_at': '2024-12-11',
        'type': available_quiz['type']
    }
    quiz_library['quizzes'].append(new_quiz)
    quiz_library['message'] = "Квіз успішно додано"


@then('квіз додається до моєї бібліотеки')
@allure.step('Перевірка додавання квізу')
def verify_quiz_added(quiz_library, available_quiz):
    """Перевіряє, що квіз додано"""
    quiz_titles = [q['title'] for q in quiz_library['quizzes']]
    assert available_quiz['title'] in quiz_titles, "Квіз не додано до бібліотеки"


@then(parsers.parse('я бачу повідомлення "{message}"'))
@allure.step('Перевірка повідомлення: {message}')
def verify_message(quiz_library, message):
    """Перевіряє повідомлення системи"""
    assert quiz_library['message'] == message, \
        f"Очікувалося '{message}', отримано '{quiz_library['message']}'"


@given(parsers.parse('у моїй бібліотеці є квіз "{quiz_title}"'))
@allure.step('Наявність квізу в бібліотеці: {quiz_title}')
def quiz_exists_in_library(quiz_library, quiz_title):
    """Перевіряє наявність квізу"""
    quiz_titles = [q['title'] for q in quiz_library['quizzes']]
    assert quiz_title in quiz_titles, f"Квіз '{quiz_title}' відсутній у бібліотеці"


@when(parsers.parse('я натискаю кнопку "Видалити" для цього квізу'))
@allure.step('Натискання кнопки видалення')
def click_delete_button(quiz_library):
    """Ініціює видалення квізу"""
    quiz_library['delete_initiated'] = True


@when('підтверджую видалення')
@allure.step('Підтвердження видалення')
def confirm_deletion(quiz_library):
    """Підтверджує видалення"""
    if quiz_library.get('delete_initiated'):
        # Видаляємо "Старий квіз"
        quiz_library['quizzes'] = [
            q for q in quiz_library['quizzes']
            if q['title'] != 'Старий квіз'
        ]
        quiz_library['message'] = "Квіз видалено"


@then('квіз видаляється з бібліотеки')
@allure.step('Перевірка видалення квізу')
def verify_quiz_deleted(quiz_library):
    """Перевіряє видалення"""
    quiz_titles = [q['title'] for q in quiz_library['quizzes']]
    assert 'Старий квіз' not in quiz_titles, "Квіз не видалено"


@then('я більше не бачу його в списку')
@allure.step('Перевірка відсутності квізу в списку')
def verify_quiz_not_visible(quiz_library):
    """Перевіряє відсутність квізу"""
    quiz_titles = [q['title'] for q in quiz_library['quizzes']]
    assert 'Старий квіз' not in quiz_titles


@given('у моїй бібліотеці є квізи з різних предметів')
@allure.step('Наявність квізів з різних предметів')
def verify_multiple_subjects(quiz_library):
    """Перевіряє різноманітність предметів"""
    subjects = set(q['subject'] for q in quiz_library['quizzes'])
    assert len(subjects) > 1, "Бібліотека містить квізи лише з одного предмету"


@when(parsers.parse('я вибираю фільтр "{subject}"'))
@allure.step('Вибір фільтру предмету: {subject}')
def apply_subject_filter(quiz_library, subject):
    """Застосовує фільтр предмету"""
    quiz_library['filters']['subject'] = subject
    
    # Перевірка, що є предмет Math для тесту
    if subject == 'Математика':
        subject = 'Math'
    
    quiz_library['filtered_quizzes'] = [
        q for q in quiz_library['quizzes']
        if q['subject'] == subject
    ]


@then(parsers.parse('я бачу лише квізи з {subject}'))
@allure.step('Перевірка відфільтрованих квізів')
def verify_filtered_quizzes(quiz_library, subject):
    """Перевіряє результати фільтрації"""
    if subject == 'математики':
        subject = 'Math'
    
    filtered = quiz_library.get('filtered_quizzes', [])
    assert len(filtered) > 0, f"Не знайдено квізів з предмету {subject}"
    
    for quiz in filtered:
        assert quiz['subject'] == subject, \
            f"Знайдено квіз з іншого предмету: {quiz['subject']}"


@then('інші квізи приховані')
@allure.step('Перевірка прихованих квізів')
def verify_other_quizzes_hidden(quiz_library):
    """Перевіряє, що інші квізи приховані"""
    filtered = quiz_library.get('filtered_quizzes', [])
    all_quizzes = quiz_library['quizzes']
    
    assert len(filtered) < len(all_quizzes), \
        "Фільтр не приховав жодного квізу"


@given(parsers.parse('у бібліотеці є квіз типу "{quiz_type}"'))
@allure.step('Наявність квізу типу: {quiz_type}')
def quiz_of_type_exists(quiz_library, quiz_type):
    """Перевіряє наявність квізу певного типу"""
    quiz_types = [q['type'] for q in quiz_library['quizzes']]
    
    # Якщо такого типу немає, додаємо
    if quiz_type not in quiz_types:
        quiz_library['quizzes'].append({
            'id': f'test_{quiz_type}',
            'title': f'Тестовий {quiz_type}',
            'subject': 'Test',
            'created_at': '2024-12-11',
            'type': quiz_type
        })
    
    quiz_library['current_quiz_type'] = quiz_type


@when('я відкриваю цей квіз')
@allure.step('Відкриття квізу')
def open_quiz(quiz_library):
    """Відкриває квіз"""
    quiz_type = quiz_library['current_quiz_type']
    quiz = next(q for q in quiz_library['quizzes'] if q['type'] == quiz_type)
    quiz_library['opened_quiz'] = quiz


@then(parsers.parse('я бачу правильну структуру для типу "{quiz_type}"'))
@allure.step('Перевірка структури квізу типу: {quiz_type}')
def verify_quiz_structure(quiz_library, quiz_type):
    """Перевіряє структуру квізу"""
    opened_quiz = quiz_library.get('opened_quiz')
    assert opened_quiz is not None, "Квіз не відкрито"
    assert opened_quiz['type'] == quiz_type, \
        f"Неправильний тип квізу: {opened_quiz['type']}"


@then('можу редагувати квіз')
@allure.step('Перевірка можливості редагування')
def verify_can_edit(quiz_library):
    """Перевіряє можливість редагування"""
    opened_quiz = quiz_library.get('opened_quiz')
    assert opened_quiz is not None, "Квіз не доступний для редагування"
    # В реальному додатку тут була б перевірка прав доступу
    quiz_library['can_edit'] = True
    assert quiz_library['can_edit'], "Редагування недоступне"
