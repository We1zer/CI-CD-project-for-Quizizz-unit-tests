
class CategoryPage:
    categories = ["Phones", "TVs", "Laptops"]
    
    def __init__(self):
        self.current_category = None
        self.breadcrumbs = []

    def open_category(self, name):
        if name not in self.categories:
            raise ValueError("Unknown category")
        self.current_category = name
        self.breadcrumbs.append(name)
        return name

    def list_subcategories(self):
        return ["sub1", "sub2", "sub3"]
    
    def get_current_category(self):
        return self.current_category
    
    def get_breadcrumbs(self):
        return list(self.breadcrumbs)
    
    def clear_breadcrumbs(self):
        self.breadcrumbs = []
        return self.breadcrumbs
    
    def is_valid_category(self, name):
        return name in self.categories
    
    def get_category_count(self):
        return len(self.categories)
    
    def add_category(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Invalid category name")
        if name in self.categories:
            raise ValueError("Category already exists")
        self.categories.append(name)
        return self.categories
    
    def remove_category(self, name):
        if name not in self.categories:
            raise ValueError("Category does not exist")
        self.categories.remove(name)
        return self.categories
