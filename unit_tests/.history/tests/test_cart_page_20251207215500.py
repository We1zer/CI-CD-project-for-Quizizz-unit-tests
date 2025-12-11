import pytest
from cart_page import CartPage


# ============== POSITIVE TESTS ==============

def test_add_item_basic():
    """Test 57: Add item to cart"""
    cart = CartPage()
    result = cart.add_item(1)
    assert 1 in result
    assert cart.get_item_count() == 1


def test_add_item_with_quantity():
    """Test 58: Add item with specific quantity"""
    cart = CartPage()
    cart.add_item(1, quantity=3)
    assert cart.get_quantity(1) == 3


def test_add_item_with_price():
    """Test 59: Add item with price"""
    cart = CartPage()
    cart.add_item(1, quantity=2, price=100.0)
    assert cart.get_total_price() == 200.0


def test_remove_item():
    """Test 60: Remove item from cart"""
    cart = CartPage()
    cart.add_item(1)
    cart.remove_item(1)
    assert 1 not in cart.get_items()


def test_get_items_empty():
    """Test 61: Get items from empty cart"""
    cart = CartPage()
    assert len(cart.get_items()) == 0


def test_get_item_count():
    """Test 62: Get correct item count"""
    cart = CartPage()
    cart.add_item(1)
    cart.add_item(2)
    assert cart.get_item_count() == 2


def test_update_quantity():
    """Test 63: Update item quantity"""
    cart = CartPage()
    cart.add_item(1, quantity=2)
    cart.update_quantity(1, 5)
    assert cart.get_quantity(1) == 5


def test_clear_cart():
    """Test 64: Clear all items from cart"""
    cart = CartPage()
    cart.add_item(1)
    cart.add_item(2)
    cart.clear_cart()
    assert cart.is_empty()


def test_is_empty_true():
    """Test 65: Cart is empty initially"""
    cart = CartPage()
    assert cart.is_empty() is True


def test_is_empty_false():
    """Test 66: Cart is not empty after adding item"""
    cart = CartPage()
    cart.add_item(1)
    assert cart.is_empty() is False


def test_has_item_true():
    """Test 67: Check if cart has specific item"""
    cart = CartPage()
    cart.add_item(5)
    assert cart.has_item(5) is True


def test_has_item_false():
    """Test 68: Check if cart doesn't have item"""
    cart = CartPage()
    assert cart.has_item(999) is False


def test_get_quantity_nonexistent():
    """Test 69: Get quantity of non-existent item returns 0"""
    cart = CartPage()
    assert cart.get_quantity(999) == 0


def test_multiple_same_items():
    """Test 70: Add same item multiple times"""
    cart = CartPage()
    cart.add_item(1, quantity=1)
    cart.add_item(1, quantity=2)
    assert cart.get_quantity(1) == 3


def test_total_price_multiple_items():
    """Test 71: Calculate total price for multiple items"""
    cart = CartPage()
    cart.add_item(1, quantity=2, price=50.0)
    cart.add_item(2, quantity=1, price=100.0)
    assert cart.get_total_price() == 200.0


def test_clear_cart_resets_price():
    """Test 72: Clear cart resets total price"""
    cart = CartPage()
    cart.add_item(1, price=100.0)
    cart.clear_cart()
    assert cart.get_total_price() == 0.0


def test_get_items_returns_copy():
    """Test 73: get_items returns independent copy"""
    cart = CartPage()
    cart.add_item(1)
    items = cart.get_items()
    items.append(999)
    assert 999 not in cart.get_items()


# ============== NEGATIVE TESTS ==============

def test_add_invalid_item_id_zero():
    """Test 74: Add item with ID 0 raises ValueError"""
    cart = CartPage()
    with pytest.raises(ValueError, match="Invalid ID"):
        cart.add_item(0)


def test_add_invalid_item_id_negative():
    """Test 75: Add item with negative ID raises ValueError"""
    cart = CartPage()
    with pytest.raises(ValueError, match="Invalid ID"):
        cart.add_item(-5)


def test_add_item_zero_quantity():
    """Test 76: Add item with zero quantity raises ValueError"""
    cart = CartPage()
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(1, quantity=0)


def test_add_item_negative_quantity():
    """Test 77: Add item with negative quantity raises ValueError"""
    cart = CartPage()
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(1, quantity=-1)


def test_add_item_negative_price():
    """Test 78: Add item with negative price raises ValueError"""
    cart = CartPage()
    with pytest.raises(ValueError, match="Price cannot be negative"):
        cart.add_item(1, price=-50.0)


def test_remove_nonexistent_item():
    """Test 79: Remove non-existent item raises ValueError"""
    cart = CartPage()
    with pytest.raises(ValueError, match="Item not in cart"):
        cart.remove_item(999)


def test_update_quantity_nonexistent_item():
    """Test 80: Update quantity of non-existent item raises ValueError"""
    cart = CartPage()
    with pytest.raises(ValueError, match="Item not in cart"):
        cart.update_quantity(999, 5)


def test_update_quantity_zero():
    """Test 81: Update quantity to zero raises ValueError"""
    cart = CartPage()
    cart.add_item(1)
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.update_quantity(1, 0)


def test_update_quantity_negative():
    """Test 82: Update quantity to negative raises ValueError"""
    cart = CartPage()
    cart.add_item(1)
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.update_quantity(1, -5)
