import pytest
from quiz_search_page import QuizSearchPage


# =============== POSITIVE TESTS ===============

def test_search_valid_query():
    """Test 57: Search for quizzes with valid query"""
    page = SearchPage()
    result = page.search("math")
    assert "quizzes" in result
    assert result["count"] >= 0

def test_search_stores_last_query():
    """Test 58: Search stores the last query"""
    page = SearchPage()
    page.search("science")
    assert page.get_last_query() == "science"

def test_search_caches_results():
    """Test 59: Search results are cached"""
    page = SearchPage()
    result1 = page.search("history")
    result2 = page.get_cached_results("history")
    assert result1 == result2

def test_sort_by_plays_ascending():
    """Test 60: Sort quizzes by plays ascending"""
    page = SearchPage()
    result = page.sort_by_plays("asc")
    assert result == "asc"

def test_sort_by_plays_descending():
    """Test 61: Sort quizzes by plays descending"""
    page = SearchPage()
    result = page.sort_by_plays("desc")
    assert result == "desc"

def test_apply_filter_subject():
    """Test 62: Apply subject filter"""
    page = SearchPage()
    result = page.apply_filter("subject", "Math")
    assert "subject" in result
    assert result["subject"] == "Math"

def test_apply_filter_grade():
    """Test 63: Apply grade level filter"""
    page = SearchPage()
    result = page.apply_filter("grade", 5)
    assert "grade" in result
    assert result["grade"] == 5

def test_apply_multiple_filters():
    """Test 64: Apply multiple filters"""
    page = SearchPage()
    page.apply_filter("subject", "Science")
    result = page.apply_filter("grade", 8)
    assert len(result) == 2
    assert result["subject"] == "Science"
    assert result["grade"] == 8

def test_clear_filters():
    """Test 65: Clear all filters"""
    page = SearchPage()
    page.apply_filter("subject", "English")
    result = page.clear_filters()
    assert len(result) == 0

def test_validate_grade_range_valid():
    """Test 66: Validate valid grade range"""
    page = SearchPage()
    result = page.validate_grade_range(3, 8)
    assert result["min"] == 3
    assert result["max"] == 8

def test_validate_grade_range_equal():
    """Test 67: Validate equal min and max grade"""
    page = SearchPage()
    result = page.validate_grade_range(5, 5)
    assert result["min"] == 5
    assert result["max"] == 5

def test_format_query_lowercase():
    """Test 68: Format query to lowercase"""
    page = SearchPage()
    result = page.format_query("MATH")
    assert result == "math"

def test_format_query_uppercase():
    """Test 69: Format query to uppercase"""
    page = SearchPage()
    result = page.format_query("math", uppercase=True)
    assert result == "MATH"

def test_multiple_searches_update_last_query():
    """Test 70: Multiple searches update last query"""
    page = SearchPage()
    page.search("science")
    page.search("history")
    assert page.get_last_query() == "history"

def test_search_with_spaces():
    """Test 71: Search with spaces in query"""
    page = SearchPage()
    result = page.search("world history")
    assert page.get_last_query() == "world history"

def test_search_unicode_query():
    """Test 72: Search with unicode characters"""
    page = SearchPage()
    result = page.search("математика")
    assert page.get_last_query() == "математика"

def test_validate_boundary_grades():
    """Test 73: Validate boundary grades (1 and 12)"""
    page = SearchPage()
    result = page.validate_grade_range(1, 12)
    assert result["min"] == 1
    assert result["max"] == 12

def test_filter_overwrite():
    """Test 74: Filter value is overwritten"""
    page = SearchPage()
    page.apply_filter("grade", 3)
    result = page.apply_filter("grade", 5)
    assert result["grade"] == 5

def test_cache_multiple_queries():
    """Test 75: Cache multiple different queries"""
    page = SearchPage()
    page.search("biology")
    page.search("chemistry")
    assert page.get_cached_results("biology") is not None
    assert page.get_cached_results("chemistry") is not None

def test_format_query_mixed_case():
    """Test 76: Format mixed case query"""
    page = SearchPage()
    result = page.format_query("MaTh QuIz")
    assert result == "math quiz"


# =============== NEGATIVE TESTS ===============

def test_search_empty_string():
    """Test 77: Search with empty string raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Invalid query"):
        page.search("")

def test_search_whitespace_only():
    """Test 78: Search with whitespace only raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Invalid query"):
        page.search("   ")

def test_search_non_string():
    """Test 79: Search with non-string raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Invalid query"):
        page.search(123)

def test_sort_invalid_order():
    """Test 80: Sort with invalid order raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Invalid sort order"):
        page.sort_by_plays("invalid")

def test_sort_empty_string():
    """Test 81: Sort with empty string raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Order must be a string"):
        page.sort_by_plays("")

def test_apply_filter_empty_name():
    """Test 82: Apply filter with empty name raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Filter name cannot be empty"):
        page.apply_filter("", "value")

def test_apply_filter_none_value():
    """Test 83: Apply filter with None value raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Filter value cannot be None"):
        page.apply_filter("subject", None)

def test_validate_grade_range_too_low():
    """Test 84: Validate grade below 1 raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Grade must be between 1 and 12"):
        page.validate_grade_range(0, 5)

def test_validate_grade_range_too_high():
    """Test 85: Validate grade above 12 raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Grade must be between 1 and 12"):
        page.validate_grade_range(5, 15)

def test_validate_grade_range_min_greater_than_max():
    """Test 86: Validate min grade > max grade raises error"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Min grade cannot exceed max grade"):
        page.validate_grade_range(8, 3)

def test_format_query_non_string():
    """Test 87: Format non-string query raises error"""
    page = SearchPage()
    with pytest.raises(TypeError, match="Query must be a string"):
        page.format_query(12345)


# =============== EDGE CASE TESTS ===============

def test_get_cached_results_nonexistent():
    """Test 88: Get cached results for non-existent query returns None"""
    page = SearchPage()
    result = page.get_cached_results("nonexistent")
    assert result is None

def test_get_last_query_before_search():
    """Test 89: Get last query before any search returns None"""
    page = SearchPage()
    assert page.get_last_query() is None
