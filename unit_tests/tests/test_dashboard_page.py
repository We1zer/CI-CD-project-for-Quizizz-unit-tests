"""
Tests for DashboardPage - Quiz dashboard functionality
"""
import pytest
from dashboard_page import DashboardPage


# =============== POSITIVE TESTS ===============

def test_dashboard_loads_default_quizzes():
    """Test 191: Dashboard loads with default quizzes"""
    page = DashboardPage()
    result = page.load_quizzes()
    assert result is True
    assert page.is_loaded is True
    assert page.get_quiz_count() == 3

def test_load_custom_quiz_list():
    """Test 192: Load custom quiz list"""
    page = DashboardPage()
    custom_quizzes = [
        {"id": 10, "name": "Custom Quiz", "subject": "Math", "grade": 6, "questions": 5, "date": "2024-02-01"}
    ]
    page.load_quizzes(custom_quizzes)
    assert page.get_quiz_count() == 1
    assert page.quizzes[0]["name"] == "Custom Quiz"

def test_search_quiz_by_name():
    """Test 193: Search for quiz by name"""
    page = DashboardPage()
    page.load_quizzes()
    results = page.search_quiz("Math")
    assert len(results) == 1
    assert results[0]["name"] == "Math Quiz"

def test_search_returns_all_on_empty_query():
    """Test 194: Empty search returns all quizzes"""
    page = DashboardPage()
    page.load_quizzes()
    results = page.search_quiz("")
    assert len(results) == 3

def test_filter_by_subject_math():
    """Test 195: Filter quizzes by Math subject"""
    page = DashboardPage()
    page.load_quizzes()
    results = page.filter_by_subject("Math")
    assert len(results) == 1
    assert results[0]["subject"] == "Math"

def test_filter_by_grade():
    """Test 196: Filter quizzes by grade level"""
    page = DashboardPage()
    page.load_quizzes()
    results = page.filter_by_grade(8)
    assert len(results) == 1
    assert results[0]["grade"] == 8

def test_sort_by_date():
    """Test 197: Sort quizzes by date (newest first)"""
    page = DashboardPage()
    page.load_quizzes()
    sorted_quizzes = page.sort_quizzes("date")
    assert sorted_quizzes[0]["date"] == "2024-01-20"
    assert sorted_quizzes[-1]["date"] == "2024-01-10"

def test_sort_by_name():
    """Test 198: Sort quizzes alphabetically by name"""
    page = DashboardPage()
    page.load_quizzes()
    sorted_quizzes = page.sort_quizzes("name")
    assert sorted_quizzes[0]["name"] == "History Exam"

def test_sort_by_questions_count():
    """Test 199: Sort quizzes by number of questions"""
    page = DashboardPage()
    page.load_quizzes()
    sorted_quizzes = page.sort_quizzes("questions")
    assert sorted_quizzes[0]["questions"] == 20
    assert sorted_quizzes[-1]["questions"] == 10

def test_click_create_quiz_button():
    """Test 200: Click Create Quiz button"""
    page = DashboardPage()
    page.load_quizzes()
    result = page.click_create_quiz_button()
    assert result["action"] == "navigate"
    assert result["url"] == "/quiz/editor/new"

def test_get_quiz_by_id():
    """Test 201: Get specific quiz by ID"""
    page = DashboardPage()
    page.load_quizzes()
    quiz = page.get_quiz_by_id(2)
    assert quiz is not None
    assert quiz["name"] == "Science Test"

def test_open_quiz():
    """Test 202: Open quiz for editing"""
    page = DashboardPage()
    page.load_quizzes()
    result = page.open_quiz(1)
    assert result["action"] == "navigate"
    assert result["url"] == "/quiz/editor/1"
    assert result["quiz"]["name"] == "Math Quiz"

def test_delete_quiz():
    """Test 203: Delete a quiz"""
    page = DashboardPage()
    page.load_quizzes()
    initial_count = page.get_quiz_count()
    result = page.delete_quiz(1)
    assert result["status"] == "success"
    assert page.get_quiz_count() == initial_count - 1

def test_clear_filters():
    """Test 204: Clear all active filters"""
    page = DashboardPage()
    page.load_quizzes()
    page.filter_by_subject("Math")
    page.search_quiz("test")
    result = page.clear_filters()
    assert result is True
    assert page.filters["subject"] is None
    assert page.search_query == ""

def test_get_active_filters():
    """Test 205: Get currently active filters"""
    page = DashboardPage()
    page.load_quizzes()
    page.filter_by_subject("Science")
    page.filter_by_grade(8)
    active = page.get_active_filters()
    assert active["subject"] == "Science"
    assert active["grade"] == 8


# =============== NEGATIVE TESTS ===============

def test_load_quizzes_with_non_list():
    """Test 206: Loading non-list raises TypeError"""
    page = DashboardPage()
    with pytest.raises(TypeError, match="Quiz list must be a list"):
        page.load_quizzes("not a list")

def test_search_with_non_string():
    """Test 207: Search with non-string raises TypeError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(TypeError, match="Search query must be a string"):
        page.search_quiz(123)

def test_filter_by_invalid_subject():
    """Test 208: Filter by invalid subject raises ValueError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(ValueError, match="Invalid subject"):
        page.filter_by_subject("InvalidSubject")

def test_filter_by_non_string_subject():
    """Test 209: Filter with non-string subject raises TypeError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(TypeError, match="Subject must be a string"):
        page.filter_by_subject(123)

def test_filter_by_non_integer_grade():
    """Test 210: Filter with non-integer grade raises TypeError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(TypeError, match="Grade must be an integer"):
        page.filter_by_grade("5")

def test_filter_by_grade_too_low():
    """Test 211: Grade below 1 raises ValueError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(ValueError, match="Grade must be between 1 and 12"):
        page.filter_by_grade(0)

def test_filter_by_grade_too_high():
    """Test 212: Grade above 12 raises ValueError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(ValueError, match="Grade must be between 1 and 12"):
        page.filter_by_grade(13)

def test_sort_by_invalid_option():
    """Test 213: Invalid sort option raises ValueError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(ValueError, match="Invalid sort option"):
        page.sort_quizzes("invalid")

def test_create_quiz_before_load():
    """Test 214: Click create button before loading raises ValueError"""
    page = DashboardPage()
    with pytest.raises(ValueError, match="Dashboard must be loaded first"):
        page.click_create_quiz_button()

def test_get_quiz_by_non_integer_id():
    """Test 215: Get quiz with non-integer ID raises TypeError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(TypeError, match="Quiz ID must be an integer"):
        page.get_quiz_by_id("1")

def test_get_quiz_by_nonexistent_id():
    """Test 216: Get quiz with nonexistent ID returns None"""
    page = DashboardPage()
    page.load_quizzes()
    quiz = page.get_quiz_by_id(999)
    assert quiz is None

def test_open_nonexistent_quiz():
    """Test 217: Open nonexistent quiz raises ValueError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(ValueError, match="Quiz with ID 999 not found"):
        page.open_quiz(999)

def test_delete_nonexistent_quiz():
    """Test 218: Delete nonexistent quiz raises ValueError"""
    page = DashboardPage()
    page.load_quizzes()
    with pytest.raises(ValueError, match="Quiz with ID 999 not found"):
        page.delete_quiz(999)


# =============== EDGE CASES ===============

def test_search_case_insensitive():
    """Test 219: Search is case insensitive"""
    page = DashboardPage()
    page.load_quizzes()
    results_lower = page.search_quiz("math")
    results_upper = page.search_quiz("MATH")
    assert len(results_lower) == len(results_upper) == 1

def test_search_with_whitespace():
    """Test 220: Search query with whitespace is trimmed"""
    page = DashboardPage()
    page.load_quizzes()
    results = page.search_quiz("  Math  ")
    assert len(results) == 1
    assert page.search_query == "Math"

def test_filter_returns_empty_list_no_match():
    """Test 221: Filter with no matches returns empty list"""
    page = DashboardPage()
    page.load_quizzes()
    results = page.filter_by_grade(11)
    assert results == []

def test_get_active_filters_when_none():
    """Test 222: Active filters is empty dict when none set"""
    page = DashboardPage()
    page.load_quizzes()
    active = page.get_active_filters()
    assert active == {}

def test_quiz_count_after_deletion():
    """Test 223: Quiz count updates after deletion"""
    page = DashboardPage()
    page.load_quizzes()
    page.delete_quiz(1)
    page.delete_quiz(2)
    assert page.get_quiz_count() == 1
