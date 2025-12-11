
class CartPage:
    def __init__(self):
        self.items = []
        self.item_quantities = {}
        self.total_price = 0.0

    def add_item(self, item_id, quantity=1, price=0.0):
        if item_id <= 0:
            raise ValueError("Invalid ID")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        self.items.append(item_id)
        self.item_quantities[item_id] = self.item_quantities.get(item_id, 0) + quantity
        self.total_price += price * quantity
        return self.items

    def remove_item(self, item_id):
        if item_id not in self.items:
            raise ValueError("Item not in cart")
        self.items.remove(item_id)
        if item_id in self.item_quantities:
            del self.item_quantities[item_id]
        return self.items

    def get_items(self):
        return list(self.items)
    
    def get_item_count(self):
        return len(self.items)
    
    def get_quantity(self, item_id):
        return self.item_quantities.get(item_id, 0)
    
    def update_quantity(self, item_id, quantity):
        if item_id not in self.items:
            raise ValueError("Item not in cart")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.item_quantities[item_id] = quantity
        return self.item_quantities[item_id]
    
    def clear_cart(self):
        self.items = []
        self.item_quantities = {}
        self.total_price = 0.0
        return self.items
    
    def get_total_price(self):
        return self.total_price
    
    def is_empty(self):
        return len(self.items) == 0
    
    def has_item(self, item_id):
        return item_id in self.items
