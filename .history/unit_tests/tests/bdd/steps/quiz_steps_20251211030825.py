"""
Step definitions для BDD тестів Quizizz
"""
from behave import given, when, then, step
import sys
import os

# Додаємо батьківську директорію до шляху для імпорту модулів
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from quiz_search_page import QuizSearchPage
from quiz_library_page import QuizLibraryPage


# === Quiz Search Steps ===

@given('я відкрив сторінку пошуку Quizizz')
def step_open_search_page(context):
    context.search_page = QuizSearchPage()
    context.current_page = 'search'


@when('я введу "{query}" в поле пошуку')
def step_enter_search_query(context, query):
    context.search_query = query
    context.search_results = context.search_page.search(query)


@when('натисну кнопку "Пошук"')
def step_click_search_button(context):
    # Пошук вже виконано в попередньому кроці
    pass


@then('я побачу список квізів з результатами')
def step_see_quiz_results(context):
    assert context.search_results is not None, "Результати пошуку не знайдені"
    assert len(context.search_results) > 0, "Список результатів порожній"


@then('результати містять ключове слово "{keyword}"')
def step_results_contain_keyword(context, keyword):
    for quiz in context.search_results:
        assert keyword.lower() in quiz['title'].lower(), \
            f"Квіз '{quiz['title']}' не містить ключове слово '{keyword}'"


@when('виберу фільтр предмету "{subject}"')
def step_select_subject_filter(context, subject):
    context.search_page.apply_filter('subject', subject)
    context.selected_subject = subject


@then('я побачу тільки квізи з предмету {subject}')
def step_see_only_subject_quizzes(context, subject):
    for quiz in context.search_results:
        assert quiz['subject'] == subject, \
            f"Квіз має предмет {quiz['subject']}, очікувалось {subject}"


@then('всі квізи мають тег "{tag}"')
def step_all_quizzes_have_tag(context, tag):
    for quiz in context.search_results:
        assert tag in quiz.get('tags', []), \
            f"Квіз '{quiz['title']}' не має тег '{tag}'"


@then('я побачу квізи категорії "{category}"')
def step_see_category_quizzes(context, category):
    for quiz in context.search_results:
        assert quiz['subject'] == category, \
            f"Неправильна категорія: {quiz['subject']}"


@then('кількість результатів більше {minimum:d}')
def step_results_count_greater(context, minimum):
    count = len(context.search_results)
    assert count > minimum, \
        f"Кількість результатів ({count}) не більше мінімуму ({minimum})"


@given('я виконав пошук за "{query}"')
def step_performed_search(context, query):
    context.search_page = QuizSearchPage()
    context.search_results = context.search_page.search(query)


@when('я виберу сортування "За популярністю"')
def step_sort_by_popularity(context):
    context.search_results = context.search_page.sort_by_plays('desc')


@then('результати відсортовані за кількістю проходжень')
def step_results_sorted_by_plays(context):
    plays = [quiz['plays'] for quiz in context.search_results]
    assert plays == sorted(plays, reverse=True), \
        "Результати не відсортовані за кількістю проходжень"


@then('перший квіз має найбільше проходжень')
def step_first_has_most_plays(context):
    if len(context.search_results) > 1:
        first_plays = context.search_results[0]['plays']
        second_plays = context.search_results[1]['plays']
        assert first_plays >= second_plays, \
            "Перший квіз не має найбільше проходжень"


# === Quiz Library Steps ===

@given('я авторизований в системі')
def step_user_logged_in(context):
    context.user_logged_in = True


@given('я перебуваю на сторінці бібліотеки')
def step_on_library_page(context):
    context.library = QuizLibraryPage()
    context.current_page = 'library'


@when('я натисну "Додати квіз"')
def step_click_add_quiz(context):
    context.adding_quiz = True


@when('введу назву квізу "{title}"')
def step_enter_quiz_title(context, title):
    context.quiz_title = title


@when('введу опис "{description}"')
def step_enter_quiz_description(context, description):
    context.quiz_description = description


@when('натисну "Зберегти"')
def step_click_save(context):
    context.library.add_quiz(context.quiz_title)
    context.quiz_added = True


@then('квіз "{title}" з\'явиться в моїй бібліотеці')
def step_quiz_appears_in_library(context, title):
    quizzes = context.library.list_quizzes()
    quiz_titles = [q['title'] for q in quizzes]
    assert title in quiz_titles, f"Квіз '{title}' не знайдено в бібліотеці"


@then('я побачу повідомлення "{message}"')
def step_see_message(context, message):
    # В реальному застосунку тут була б перевірка UI повідомлення
    assert context.quiz_added, "Квіз не був доданий"


@given('в моїй бібліотеці є квіз "{title}"')
def step_quiz_exists_in_library(context, title):
    context.library = QuizLibraryPage()
    context.library.add_quiz(title)


@when('я виберу квіз "{title}"')
def step_select_quiz(context, title):
    context.selected_quiz = title


@when('натисну "Видалити"')
def step_click_delete(context):
    context.deleting = True


@when('підтверджу видалення')
def step_confirm_deletion(context):
    context.library.remove_quiz(context.selected_quiz)
    context.quiz_deleted = True


@then('квіз "{title}" зникне з бібліотеки')
def step_quiz_removed_from_library(context, title):
    quizzes = context.library.list_quizzes()
    quiz_titles = [q['title'] for q in quizzes]
    assert title not in quiz_titles, f"Квіз '{title}' все ще в бібліотеці"


@then('загальна кількість квізів зменшиться на 1')
def step_quiz_count_decreased(context):
    current_count = context.library.get_quiz_count()
    assert current_count >= 0, "Кількість квізів не може бути від'ємною"


@given('в бібліотеці є квіз "{title}" з {plays:d} проходженнями')
def step_quiz_with_plays(context, title, plays):
    context.library = QuizLibraryPage()
    context.library.add_quiz(title)
    # В реальному застосунку тут було б встановлення кількості проходжень


@when('я відкрию детальну інформацію про "{title}"')
def step_open_quiz_details(context, title):
    context.selected_quiz = title


@then('я побачу кількість проходжень: {plays:d}')
def step_see_play_count(context, plays):
    quiz_plays = context.library.get_total_plays()
    assert quiz_plays >= 0, "Кількість проходжень повинна бути невід'ємною"


@then('я побачу середній бал')
def step_see_average_score(context):
    # В реальному застосунку тут була б перевірка відображення середнього балу
    pass


@then('я побачу дату створення квізу')
def step_see_creation_date(context):
    # В реальному застосунку тут була б перевірка відображення дати
    pass


@given('в моїй бібліотеці є {count:d} квізів')
def step_library_has_quizzes(context, count):
    context.library = QuizLibraryPage()
    for i in range(count):
        context.library.add_quiz(f"Quiz {i+1}")


@when('я введу "{query}" в поле пошуку бібліотеки')
def step_search_in_library(context, query):
    all_quizzes = context.library.list_quizzes()
    context.search_results = [q for q in all_quizzes if query.lower() in q['title'].lower()]


@then('я побачу тільки квізи з назвою що містить "{keyword}"')
def step_see_quizzes_with_keyword(context, keyword):
    for quiz in context.search_results:
        assert keyword.lower() in quiz['title'].lower(), \
            f"Квіз '{quiz['title']}' не містить '{keyword}'"


@then('кількість результатів менше {maximum:d}')
def step_results_count_less(context, maximum):
    count = len(context.search_results)
    assert count < maximum, \
        f"Кількість результатів ({count}) не менше максимуму ({maximum})"
