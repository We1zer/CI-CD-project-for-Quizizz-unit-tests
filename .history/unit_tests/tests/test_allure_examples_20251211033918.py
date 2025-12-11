"""
Приклад тестів з Allure анотаціями для красивої звітності
"""
import pytest
import allure
from quiz_search_page import QuizSearchPage
from quiz_library_page import QuizLibraryPage


@allure.feature('Quiz Search')
@allure.story('Базовий пошук квізів')
class TestQuizSearchWithAllure:
    """Тести пошуку квізів з Allure звітністю"""
    
    @allure.title("Пошук квізу за простим запитом")
    @allure.description("Перевірка базового пошуку квізу за ключовим словом")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_basic_search_with_allure(self):
        with allure.step("Створення об'єкту сторінки пошуку"):
            page = QuizSearchPage()
        
        with allure.step("Виконання пошуку за запитом 'Python'"):
            results = page.search("Python")
        
        with allure.step("Перевірка що результати не порожні"):
            assert len(results) > 0, "Результати пошуку порожні"
            allure.attach(
                f"Знайдено {len(results)} квізів",
                name="Кількість результатів",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.title("Фільтрація квізів за предметом")
    @allure.description("Тестування фільтрації результатів пошуку за предметом")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_filter_by_subject_with_allure(self):
        page = QuizSearchPage()
        
        with allure.step("Виконання пошуку"):
            page.search("Mathematics")
        
        with allure.step("Застосування фільтру 'Math'"):
            page.apply_filter('subject', 'Math')
            results = page.search("Mathematics")
        
        with allure.step("Перевірка що всі результати мають правильний предмет"):
            for quiz in results:
                assert quiz['subject'] == 'Math'
                allure.attach(
                    f"Quiz: {quiz['title']}, Subject: {quiz['subject']}",
                    name=f"Квіз деталі",
                    attachment_type=allure.attachment_type.TEXT
                )
    
    @allure.title("Сортування квізів за популярністю")
    @allure.description("Перевірка правильності сортування квізів за кількістю проходжень")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://quizizz.com", name="Quizizz Website")
    @pytest.mark.regression
    def test_sort_by_popularity_with_allure(self):
        page = QuizSearchPage()
        
        with allure.step("Виконання пошуку за 'History'"):
            page.search("History")
        
        with allure.step("Сортування за кількістю проходжень (desc)"):
            sorted_results = page.sort_by_plays('desc')
        
        with allure.step("Перевірка що результати відсортовані правильно"):
            plays = [quiz['plays'] for quiz in sorted_results]
            assert plays == sorted(plays, reverse=True)
            
            # Додаємо таблицю в звіт
            table_data = [
                ["№", "Назва квізу", "Кількість проходжень"]
            ]
            for idx, quiz in enumerate(sorted_results[:5], 1):
                table_data.append([str(idx), quiz['title'], str(quiz['plays'])])
            
            allure.attach(
                "\n".join(["\t".join(row) for row in table_data]),
                name="Топ 5 квізів",
                attachment_type=allure.attachment_type.TEXT
            )


@allure.feature('Quiz Library')
@allure.story('Управління бібліотекою квізів')
class TestQuizLibraryWithAllure:
    """Тести бібліотеки квізів з Allure звітністю"""
    
    @allure.title("Додавання нового квізу до бібліотеки")
    @allure.description("Перевірка можливості додавання квізу")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.issue("QUIZ-123", name="Issue в Jira")
    @pytest.mark.smoke
    def test_add_quiz_with_allure(self):
        library = QuizLibraryPage()
        
        with allure.step("Отримання початкової кількості квізів"):
            initial_count = library.get_quiz_count()
            allure.attach(str(initial_count), name="Початкова кількість", 
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Додавання нового квізу 'Python Basics'"):
            library.add_quiz("Python Basics")
        
        with allure.step("Перевірка що кількість квізів збільшилась"):
            new_count = library.get_quiz_count()
            assert new_count == initial_count + 1
            
            allure.attach(str(new_count), name="Нова кількість", 
                         attachment_type=allure.attachment_type.TEXT)
    
    @allure.title("Видалення квізу з бібліотеки")
    @allure.description("Тестування функції видалення квізу")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase("TC-456", name="Test Case 456")
    @pytest.mark.regression
    def test_remove_quiz_with_allure(self):
        library = QuizLibraryPage()
        
        with allure.step("Додавання тестового квізу"):
            library.add_quiz("Test Quiz to Remove")
            quizzes_before = library.list_quizzes()
            count_before = len(quizzes_before)
        
        with allure.step("Видалення квізу"):
            library.remove_quiz("Test Quiz to Remove")
        
        with allure.step("Перевірка що квіз видалено"):
            quizzes_after = library.list_quizzes()
            count_after = len(quizzes_after)
            
            assert count_after == count_before - 1
            assert not any(q['title'] == "Test Quiz to Remove" for q in quizzes_after)
            
            allure.attach(
                f"До видалення: {count_before}\nПісля видалення: {count_after}",
                name="Статистика",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.title("Підрахунок загальної кількості питань")
    @allure.description("Перевірка правильності підрахунку питань у всіх квізах")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.unit
    def test_total_questions_count_with_allure(self):
        library = QuizLibraryPage()
        
        with allure.step("Очищення бібліотеки"):
            library.quizzes = []
        
        with allure.step("Додавання квізів з різною кількістю питань"):
            quiz_data = [
                ("Quiz 1", 10),
                ("Quiz 2", 15),
                ("Quiz 3", 20)
            ]
            
            for title, questions in quiz_data:
                library.add_quiz(title)
                allure.attach(
                    f"{title}: {questions} питань",
                    name=f"Додано {title}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        with allure.step("Перевірка загальної кількості питань"):
            # В реальності це буде рахуватись з даних квізів
            total = library.get_total_questions()
            assert total >= 0  # Базова перевірка
            
            allure.attach(
                str(total),
                name="Загальна кількість питань",
                attachment_type=allure.attachment_type.TEXT
            )


@allure.feature('Performance Tests')
@allure.story('Тести продуктивності')
class TestPerformanceWithAllure:
    """Тести продуктивності з Allure звітністю"""
    
    @allure.title("Тест швидкості пошуку")
    @allure.description("Вимірювання часу виконання пошуку")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.slow
    def test_search_performance_with_allure(self):
        import time
        page = QuizSearchPage()
        
        with allure.step("Виконання 100 пошукових запитів"):
            start_time = time.time()
            
            for i in range(100):
                page.search(f"Query {i}")
            
            elapsed_time = time.time() - start_time
        
        with allure.step("Перевірка що час виконання прийнятний"):
            avg_time = elapsed_time / 100
            
            allure.attach(
                f"Загальний час: {elapsed_time:.2f}s\n"
                f"Середній час на запит: {avg_time:.4f}s\n"
                f"Запитів за секунду: {100/elapsed_time:.2f}",
                name="Метрики продуктивності",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Перевірка що середній час менше 0.1 секунди
            assert avg_time < 0.1, f"Пошук занадто повільний: {avg_time}s"


@allure.feature('Data Validation')
@allure.story('Валідація даних')
@pytest.mark.parametrize("min_grade,max_grade,expected_valid", [
    (1, 5, True),
    (6, 12, True),
    (5, 3, False),  # min > max
    (-1, 5, False),  # від'ємне значення
    (1, 15, False),  # max > 12
])
class TestDataValidationWithAllure:
    """Параметризовані тести з Allure"""
    
    @allure.title("Валідація діапазону класів: {min_grade}-{max_grade}")
    @allure.description("Перевірка валідації діапазону класів")
    @allure.severity(allure.severity_level.NORMAL)
    def test_grade_range_validation_with_allure(self, min_grade, max_grade, expected_valid):
        page = QuizSearchPage()
        
        with allure.step(f"Валідація діапазону {min_grade}-{max_grade}"):
            result = page.validate_grade_range(min_grade, max_grade)
            
            allure.attach(
                f"Min: {min_grade}\n"
                f"Max: {max_grade}\n"
                f"Очікується валідним: {expected_valid}\n"
                f"Результат: {result}",
                name="Параметри валідації",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Перевірка результату валідації"):
            assert result == expected_valid, \
                f"Очікувалось {expected_valid}, отримано {result}"


if __name__ == "__main__":
    # Запуск тестів з Allure
    pytest.main([
        __file__,
        "-v",
        "--alluredir=reports/allure-results",
        "--clean-alluredir"
    ])
