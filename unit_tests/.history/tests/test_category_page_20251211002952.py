import pytest
from category_page import CategoryPage


# ============== POSITIVE TESTS ==============

def test_open_category_phones():
    """Test 34: Open Phones category"""
    page = CategoryPage()
    result = page.open_category("Phones")
    assert result == "Phones"
    assert page.get_current_category() == "Phones"


def test_open_category_tvs():
    """Test 35: Open TVs category"""
    page = CategoryPage()
    result = page.open_category("TVs")
    assert result == "TVs"


def test_open_category_laptops():
    """Test 36: Open Laptops category"""
    page = CategoryPage()
    result = page.open_category("Laptops")
    assert result == "Laptops"


def test_list_subcategories():
    """Test 37: List all subcategories"""
    page = CategoryPage()
    subs = page.list_subcategories()
    assert len(subs) == 3
    assert "sub1" in subs


def test_get_current_category_initial():
    """Test 38: Get current category initially returns None"""
    page = CategoryPage()
    assert page.get_current_category() is None


def test_breadcrumbs_single_category():
    """Test 39: Breadcrumbs contain single category after opening"""
    page = CategoryPage()
    page.open_category("Phones")
    crumbs = page.get_breadcrumbs()
    assert len(crumbs) == 1
    assert crumbs[0] == "Phones"


def test_breadcrumbs_multiple_categories():
    """Test 40: Breadcrumbs track multiple category opens"""
    page = CategoryPage()
    page.open_category("Phones")
    page.open_category("TVs")
    crumbs = page.get_breadcrumbs()
    assert len(crumbs) == 2
    assert crumbs == ["Phones", "TVs"]


def test_clear_breadcrumbs():
    """Test 41: Clear breadcrumbs removes all entries"""
    page = CategoryPage()
    page.open_category("Laptops")
    page.clear_breadcrumbs()
    assert len(page.get_breadcrumbs()) == 0


def test_is_valid_category_phones():
    """Test 42: Validate existing category Phones"""
    page = CategoryPage()
    assert page.is_valid_category("Phones") is True


def test_is_valid_category_invalid():
    """Test 43: Validate non-existing category returns False"""
    page = CategoryPage()
    assert page.is_valid_category("InvalidCategory") is False


def test_get_category_count_default():
    """Test 44: Get default category count"""
    page = CategoryPage()
    assert page.get_category_count() == 3


def test_add_new_category():
    """Test 45: Add a new category"""
    page = CategoryPage()
    result = page.add_category("Tablets")
    assert "Tablets" in result
    assert page.get_category_count() == 4


def test_remove_existing_category():
    """Test 46: Remove an existing category"""
    page = CategoryPage()
    initial_count = page.get_category_count()
    result = page.remove_category("Phones")
    assert "Phones" not in result
    assert page.get_category_count() == initial_count - 1


def test_category_state_persistence():
    """Test 47: Current category persists after multiple operations"""
    page = CategoryPage()
    page.open_category("Laptops")
    page.list_subcategories()
    assert page.get_current_category() == "Laptops"


def test_breadcrumbs_independence():
    """Test 48: Breadcrumbs list is independent copy"""
    page = CategoryPage()
    page.open_category("TVs")
    crumbs1 = page.get_breadcrumbs()
    crumbs1.append("Modified")
    crumbs2 = page.get_breadcrumbs()
    assert "Modified" not in crumbs2


def test_add_category_with_spaces():
    """Test 49: Add category with spaces in name"""
    page = CategoryPage()
    page.add_category("Smart Watches")
    assert page.is_valid_category("Smart Watches")


# ============== NEGATIVE TESTS ==============

def test_open_invalid_category():
    """Test 50: Opening invalid category raises ValueError"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Unknown category"):
        page.open_category("InvalidCat")


def test_add_duplicate_category():
    """Test 51: Adding duplicate category raises ValueError"""
    page = CategoryPage()
    page.add_category("NewCategory")
    with pytest.raises(ValueError, match="Category already exists"):
        page.add_category("NewCategory")


def test_add_empty_category():
    """Test 52: Adding empty category name raises ValueError"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Invalid category name"):
        page.add_category("")


def test_add_none_category():
    """Test 53: Adding None as category raises ValueError"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Invalid category name"):
        page.add_category(None)


def test_add_non_string_category():
    """Test 54: Adding non-string category raises ValueError"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Invalid category name"):
        page.add_category(123)


def test_remove_nonexistent_category():
    """Test 55: Removing non-existent category raises ValueError"""
    page = CategoryPage()
    with pytest.raises(ValueError, match="Category does not exist"):
        page.remove_category("NonExistent")


def test_breadcrumbs_before_opening():
    """Test 56: Breadcrumbs empty before opening any category"""
    page = CategoryPage()
    assert len(page.get_breadcrumbs()) == 0
