import pytest
from search_page import SearchPage


# ============== POSITIVE TESTS ==============

def test_search_valid_query():
    """Test 1: Search with valid query string"""
    page = SearchPage()
    result = page.search("laptop")
    assert result["results"][0] == "laptop"
    assert result["count"] == 1


def test_search_stores_last_query():
    """Test 2: Test that search stores the last query"""
    page = SearchPage()
    page.search("phone")
    assert page.get_last_query() == "phone"


def test_search_caches_results():
    """Test 3: Test that search results are cached"""
    page = SearchPage()
    page.search("tablet")
    cached = page.get_cached_results("tablet")
    assert cached is not None
    assert cached["results"][0] == "tablet"


def test_sort_by_price_ascending():
    """Test 4: Test sorting by price in ascending order"""
    page = SearchPage()
    result = page.sort_by_price("asc")
    assert result == "asc"


def test_sort_by_price_descending():
    """Test 5: Test sorting by price in descending order"""
    page = SearchPage()
    result = page.sort_by_price("desc")
    assert result == "desc"


def test_apply_filter_brand():
    """Test 6: Test applying brand filter"""
    page = SearchPage()
    filters = page.apply_filter("brand", "Samsung")
    assert "brand" in filters
    assert filters["brand"] == "Samsung"


def test_apply_filter_price():
    """Test 7: Test applying price filter"""
    page = SearchPage()
    filters = page.apply_filter("price", "1000-5000")
    assert filters["price"] == "1000-5000"


def test_apply_multiple_filters():
    """Test 8: Test applying multiple filters"""
    page = SearchPage()
    page.apply_filter("brand", "Apple")
    page.apply_filter("color", "Black")
    assert len(page.filters) == 2


def test_clear_filters():
    """Test 9: Test clearing all filters"""
    page = SearchPage()
    page.apply_filter("brand", "LG")
    page.clear_filters()
    assert len(page.filters) == 0


def test_validate_price_range_valid():
    """Test 10: Test validating valid price range"""
    page = SearchPage()
    result = page.validate_price_range(100, 1000)
    assert result["min"] == 100
    assert result["max"] == 1000


def test_validate_price_range_equal():
    """Test 11: Test validating price range with equal values"""
    page = SearchPage()
    result = page.validate_price_range(500, 500)
    assert result["min"] == 500
    assert result["max"] == 500


def test_format_query_lowercase():
    """Test 12: Test formatting query to lowercase"""
    page = SearchPage()
    result = page.format_query("LAPTOP")
    assert result == "laptop"


def test_format_query_uppercase():
    """Test 13: Test formatting query to uppercase"""
    page = SearchPage()
    result = page.format_query("laptop", uppercase=True)
    assert result == "LAPTOP"


def test_multiple_searches_update_last_query():
    """Test 14: Test that multiple searches update last query"""
    page = SearchPage()
    page.search("first")
    page.search("second")
    assert page.get_last_query() == "second"


def test_search_with_spaces():
    """Test 15: Test search with query containing spaces"""
    page = SearchPage()
    result = page.search("gaming laptop")
    assert result["results"][0] == "gaming laptop"


def test_search_unicode_query():
    """Test 16: Test search with Unicode characters"""
    page = SearchPage()
    result = page.search("ноутбук")
    assert result["results"][0] == "ноутбук"


def test_validate_zero_prices():
    """Test 17: Test validating price range with zero values"""
    page = SearchPage()
    result = page.validate_price_range(0, 0)
    assert result["min"] == 0
    assert result["max"] == 0


def test_filter_overwrite():
    """Test 18: Test that filter values can be overwritten"""
    page = SearchPage()
    page.apply_filter("brand", "Samsung")
    page.apply_filter("brand", "Apple")
    assert page.filters["brand"] == "Apple"


def test_cache_multiple_queries():
    """Test 19: Test caching multiple different queries"""
    page = SearchPage()
    page.search("query1")
    page.search("query2")
    assert page.get_cached_results("query1") is not None
    assert page.get_cached_results("query2") is not None


def test_format_query_mixed_case():
    """Test 20: Test formatting mixed case query"""
    page = SearchPage()
    result = page.format_query("LaPtOp")
    assert result == "laptop"


# ============== NEGATIVE TESTS ==============

def test_search_empty_string():
    """Test 21: Test search with empty string raises ValueError"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Invalid query"):
        page.search("")


def test_search_whitespace_only():
    """Test 22: Test search with whitespace only raises ValueError"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Invalid query"):
        page.search("   ")


def test_search_non_string():
    """Test 23: Test search with non-string type raises ValueError"""
    page = SearchPage()
    with pytest.raises(ValueError):
        page.search(123)


def test_sort_invalid_order():
    """Test 24: Test sort with invalid order raises ValueError"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Invalid sort order"):
        page.sort_by_price("invalid")


def test_sort_empty_string():
    """Test 25: Test sort with empty string raises ValueError"""
    page = SearchPage()
    with pytest.raises(ValueError):
        page.sort_by_price("")


def test_apply_filter_empty_name():
    """Test 26: Test applying filter with empty name raises ValueError"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Filter name cannot be empty"):
        page.apply_filter("", "value")


def test_apply_filter_none_value():
    """Test 27: Test applying filter with None value raises ValueError"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Filter value cannot be None"):
        page.apply_filter("brand", None)


def test_validate_price_range_negative_min():
    """Test 28: Test price validation with negative min price"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Prices cannot be negative"):
        page.validate_price_range(-100, 1000)


def test_validate_price_range_negative_max():
    """Test 29: Test price validation with negative max price"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Prices cannot be negative"):
        page.validate_price_range(100, -1000)


def test_validate_price_range_min_greater_than_max():
    """Test 30: Test price validation when min > max"""
    page = SearchPage()
    with pytest.raises(ValueError, match="Min price cannot exceed max price"):
        page.validate_price_range(1000, 100)


def test_format_query_non_string():
    """Test 31: Test format query with non-string raises TypeError"""
    page = SearchPage()
    with pytest.raises(TypeError, match="Query must be a string"):
        page.format_query(123)


def test_get_cached_results_nonexistent():
    """Test 32: Test getting cached results for nonexistent query returns None"""
    page = SearchPage()
    result = page.get_cached_results("nonexistent")
    assert result is None


def test_get_last_query_before_search():
    """Test 33: Test getting last query before any search returns None"""
    page = SearchPage()
    assert page.get_last_query() is None
