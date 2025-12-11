import pytest
from quiz_search_page import QuizSearchPage


# =============== POSITIVE TESTS ===============

def test_search_valid_query():
    """Test 57: Пошук квізів з валідним запитом"""
    page = QuizSearchPage()
    result = page.search("math")
    assert "quizzes" in result
    assert result["count"] >= 0

def test_search_stores_last_query():
    """Test 58: Пошук зберігає останній запит"""
    page = QuizSearchPage()
    page.search("science")
    assert page.get_last_query() == "science"

def test_search_caches_results():
    """Test 59: Результати пошуку кешуються"""
    page = QuizSearchPage()
    result1 = page.search("history")
    result2 = page.get_cached_results("history")
    assert result1 == result2

def test_sort_by_plays_ascending():
    """Test 60: Сортування квізів за кількістю проходжень (зростання)"""
    page = QuizSearchPage()
    result = page.sort_by_plays("asc")
    assert result == "asc"

def test_sort_by_plays_descending():
    """Test 61: Сортування квізів за кількістю проходжень (спадання)"""
    page = QuizSearchPage()
    result = page.sort_by_plays("desc")
    assert result == "desc"

def test_apply_filter_subject():
    """Test 62: Застосування фільтру за предметом"""
    page = QuizSearchPage()
    result = page.apply_filter("subject", "Math")
    assert "subject" in result
    assert result["subject"] == "Math"

def test_apply_filter_grade():
    """Test 63: Застосування фільтру за класом"""
    page = QuizSearchPage()
    result = page.apply_filter("grade", 5)
    assert "grade" in result
    assert result["grade"] == 5

def test_apply_multiple_filters():
    """Test 64: Застосування кількох фільтрів"""
    page = QuizSearchPage()
    page.apply_filter("subject", "Science")
    result = page.apply_filter("grade", 8)
    assert len(result) == 2
    assert result["subject"] == "Science"
    assert result["grade"] == 8

def test_clear_filters():
    """Test 65: Очищення всіх фільтрів"""
    page = QuizSearchPage()
    page.apply_filter("subject", "English")
    result = page.clear_filters()
    assert len(result) == 0

def test_validate_grade_range_valid():
    """Test 66: Валідація коректного діапазону класів"""
    page = QuizSearchPage()
    result = page.validate_grade_range(3, 8)
    assert result["min"] == 3
    assert result["max"] == 8

def test_validate_grade_range_equal():
    """Test 67: Валідація однакових мінімального та максимального класів"""
    page = QuizSearchPage()
    result = page.validate_grade_range(5, 5)
    assert result["min"] == 5
    assert result["max"] == 5

def test_format_query_lowercase():
    """Test 68: Форматування запиту до нижнього регістру"""
    page = QuizSearchPage()
    result = page.format_query("MATH")
    assert result == "math"

def test_format_query_uppercase():
    """Test 69: Форматування запиту до верхнього регістру"""
    page = QuizSearchPage()
    result = page.format_query("math", uppercase=True)
    assert result == "MATH"

def test_multiple_searches_update_last_query():
    """Test 70: Кілька пошуків оновлюють останній запит"""
    page = QuizSearchPage()
    page.search("science")
    page.search("history")
    assert page.get_last_query() == "history"

def test_search_with_spaces():
    """Test 71: Пошук з пробілами в запиті"""
    page = QuizSearchPage()
    result = page.search("world history")
    assert page.get_last_query() == "world history"

def test_search_unicode_query():
    """Test 72: Пошук з unicode символами"""
    page = QuizSearchPage()
    result = page.search("математика")
    assert page.get_last_query() == "математика"

def test_validate_boundary_grades():
    """Test 73: Валідація граничних класів (1 та 12)"""
    page = QuizSearchPage()
    result = page.validate_grade_range(1, 12)
    assert result["min"] == 1
    assert result["max"] == 12

def test_filter_overwrite():
    """Test 74: Значення фільтру перезаписується"""
    page = QuizSearchPage()
    page.apply_filter("grade", 3)
    result = page.apply_filter("grade", 5)
    assert result["grade"] == 5

def test_cache_multiple_queries():
    """Test 75: Кешування кількох різних запитів"""
    page = QuizSearchPage()
    page.search("biology")
    page.search("chemistry")
    assert page.get_cached_results("biology") is not None
    assert page.get_cached_results("chemistry") is not None

def test_format_query_mixed_case():
    """Test 76: Форматування запиту зі змішаним регістром"""
    page = QuizSearchPage()
    result = page.format_query("MaTh QuIz")
    assert result == "math quiz"


# =============== NEGATIVE TESTS ===============

def test_search_empty_string():
    """Test 77: Пошук з порожнім рядком викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Invalid query"):
        page.search("")

def test_search_whitespace_only():
    """Test 78: Пошук тільки з пробілами викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Invalid query"):
        page.search("   ")

def test_search_non_string():
    """Test 79: Пошук з не-рядком викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Invalid query"):
        page.search(123)

def test_sort_invalid_order():
    """Test 80: Сортування з неправильним порядком викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Invalid sort order"):
        page.sort_by_plays("invalid")

def test_sort_empty_string():
    """Test 81: Сортування з порожнім рядком викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Order must be a string"):
        page.sort_by_plays("")

def test_apply_filter_empty_name():
    """Test 82: Застосування фільтру з порожньою назвою викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Filter name cannot be empty"):
        page.apply_filter("", "value")

def test_apply_filter_none_value():
    """Test 83: Застосування фільтру зі значенням None викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Filter value cannot be None"):
        page.apply_filter("subject", None)

def test_validate_grade_range_too_low():
    """Test 84: Валідація класу нижче 1 викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Grade must be between 1 and 12"):
        page.validate_grade_range(0, 5)

def test_validate_grade_range_too_high():
    """Test 85: Валідація класу вище 12 викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Grade must be between 1 and 12"):
        page.validate_grade_range(5, 15)

def test_validate_grade_range_min_greater_than_max():
    """Test 86: Валідація мін. класу > макс. класу викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(ValueError, match="Min grade cannot exceed max grade"):
        page.validate_grade_range(8, 3)

def test_format_query_non_string():
    """Test 87: Форматування не-рядкового запиту викликає помилку"""
    page = QuizSearchPage()
    with pytest.raises(TypeError, match="Query must be a string"):
        page.format_query(12345)


# =============== EDGE CASE TESTS ===============

def test_get_cached_results_nonexistent():
    """Test 88: Отримання кешованих результатів для неіснуючого запиту повертає None"""
    page = QuizSearchPage()
    result = page.get_cached_results("nonexistent")
    assert result is None

def test_get_last_query_before_search():
    """Test 89: Отримання останнього запиту до будь-якого пошуку повертає None"""
    page = QuizSearchPage()
    assert page.get_last_query() is None
