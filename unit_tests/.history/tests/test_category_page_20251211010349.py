import pytest
from category_page import CategoryPage


# =============== POSITIVE TESTS ===============

def test_open_category_math():
    """Test 40: Open Math category"""
    page = CategoryPage()
    result = page.open_category("Math")
    assert result == "Math"

def test_open_category_science():
    """Test 41: Open Science category"""
    page = CategoryPage()
    result = page.open_category("Science")
    assert result == "Science"

def test_open_category_history():
    """Test 42: Open History category"""
    page = CategoryPage()
    result = page.open_category("History")
    assert result == "History"

def test_list_subcategories():
    """Test 43: List subcategories returns topics"""
    page = CategoryPage()
    result = page.list_subcategories()
    assert len(result) == 3
    assert "topic1" in result

def test_get_current_category_initial():
    """Test 44: Initial current category is None"""
    page = CategoryPage()
    assert page.get_current_category() is None

def test_breadcrumbs_single_category():
    """Test 45: Breadcrumbs track single category"""
    page = CategoryPage()
    page.open_category("Math")
    breadcrumbs = page.get_breadcrumbs()
    assert len(breadcrumbs) == 1
    assert "Math" in breadcrumbs

def test_breadcrumbs_multiple_categories():
    """Test 46: Breadcrumbs track multiple categories"""
    page = CategoryPage()
    page.open_category("Math")
    page.open_category("Science")
    breadcrumbs = page.get_breadcrumbs()
    assert len(breadcrumbs) == 2
    assert "Math" in breadcrumbs
    assert "Science" in breadcrumbs

def test_clear_breadcrumbs():
    """Test 47: Clear breadcrumbs empties the list"""
    page = CategoryPage()
    page.open_category("History")
    result = page.clear_breadcrumbs()
    assert len(result) == 0

def test_is_valid_category_math():
    """Test 48: Math is a valid category"""
    page = CategoryPage()
    assert page.is_valid_category("Math") is True

def test_is_valid_category_invalid():
    """Test 49: Invalid category returns False"""
    page = CategoryPage()
    assert page.is_valid_category("InvalidSubject") is False

def test_get_category_count_default():
    """Test 50: Default category count is 5"""
    page = CategoryPage()
    assert page.get_category_count() == 5

def test_add_new_category():
    """Test 51: Add new category increases count"""
    page = CategoryPage()
    result = page.add_category("Physics")
    assert "Physics" in result
    assert page.get_category_count() == 6

def test_remove_existing_category():
    """Test 52: Remove an existing category"""
    page = CategoryPage()
    initial_count = page.get_category_count()
    result = page.remove_category("Math")
    assert "Math" not in result
    assert page.get_category_count() == initial_count - 1

def test_category_state_persistence():
    """Test 53: Current category persists after multiple operations"""
    page = CategoryPage()
    page.open_category("History")
    page.list_subcategories()
    assert page.get_current_category() == "History"

def test_breadcrumbs_independence():
    """Test 54: Breadcrumbs are independent copies"""
    page = CategoryPage()
    page.open_category("English")
    breadcrumbs1 = page.get_breadcrumbs()
    breadcrumbs1.append("fake")
    breadcrumbs2 = page.get_breadcrumbs()
    assert len(breadcrumbs2) == 1

def test_add_category_with_spaces():
    """Test 55: Add category with spaces in name"""
    page = CategoryPage()
    result = page.add_category("World History")
    assert "World History" in result


# =============== NEGATIVE TESTS ===============

def test_open_invalid_category():
    """Test 56: Opening invalid category raises error"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Unknown category"):
        page.open_category("InvalidSubject")

def test_add_duplicate_category():
    """Test 57: Adding duplicate category raises ValueError"""
    page = CategoryPage()
    page.add_category("NewSubject")
    with pytest.raises(ValueError, match="Category already exists"):
        page.add_category("NewSubject")

def test_add_empty_category():
    """Test 58: Adding empty category raises error"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Invalid category name"):
        page.add_category("")

def test_add_none_category():
    """Test 59: Adding None category raises error"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Invalid category name"):
        page.add_category(None)

def test_add_non_string_category():
    """Test 60: Adding non-string category raises error"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Invalid category name"):
        page.add_category(123)

def test_remove_nonexistent_category():
    """Test 61: Removing nonexistent category raises error"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Category does not exist"):
        page.remove_category("NonExistent")


# =============== EDGE CASE TESTS ===============

def test_breadcrumbs_before_opening():
    """Test 62: Breadcrumbs are empty before opening any category"""
    page = CategoryPage()
    breadcrumbs = page.get_breadcrumbs()
    assert len(breadcrumbs) == 0
