
class CategoryPage:
    """Quizizz categories - subjects like Math, Science, History"""
    
    def __init__(self):
        self.categories = ["Math", "Science", "History", "English", "Geography"]
        self.current_category = None
        self.breadcrumbs = []

    def open_category(self, name):
        """Navigate to a subject category"""
        if name not in self.categories:
            raise ValueError("Unknown category")
        self.current_category = name
        self.breadcrumbs.append(name)
        return name

    def list_subcategories(self):
        """List sub-topics in current category"""
        return ["topic1", "topic2", "topic3"]
    
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
        """Add new subject category"""
        if not name or not isinstance(name, str):
            raise ValueError("Invalid category name")
        if name in self.categories:
            raise ValueError("Category already exists")
        self.categories.append(name)
        return self.categories
    
    def remove_category(self, name):
        """Remove subject category"""
        if name not in self.categories:
            raise ValueError("Category does not exist")
        self.categories.remove(name)
        return self.categories
