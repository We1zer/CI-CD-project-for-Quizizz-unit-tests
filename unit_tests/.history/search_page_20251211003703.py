
class SearchPage:
    """Quizizz search functionality - search for quizzes, apply filters"""
    def __init__(self):
        self.last_query = None
        self.filters = {}
        self.results_cache = {}
    
    def search(self, query):
        """Search for quizzes by keyword"""
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Invalid query")
        self.last_query = query
        results = {"quizzes": [query], "count": 1}
        self.results_cache[query] = results
        return results

    def sort_by_plays(self, order):
        """Sort quizzes by number of plays"""
        if order not in ("asc", "desc"):
            raise ValueError("Invalid sort order")
        return order
    
    def apply_filter(self, filter_name, value):
        """Apply filter: grade, subject, language"""
        if not filter_name:
            raise ValueError("Filter name cannot be empty")
        if value is None:
            raise ValueError("Filter value cannot be None")
        self.filters[filter_name] = value
        return self.filters
    
    def clear_filters(self):
        self.filters = {}
        return self.filters
    
    def get_cached_results(self, query):
        return self.results_cache.get(query)
    
    def get_last_query(self):
        return self.last_query
    
    def validate_grade_range(self, min_grade, max_grade):
        """Validate grade range (1-12)"""
        if min_grade < 1 or max_grade > 12:
            raise ValueError("Grade must be between 1 and 12")
        if min_grade > max_grade:
            raise ValueError("Min grade cannot exceed max grade")
        return {"min": min_grade, "max": max_grade}
    
    def format_query(self, query, uppercase=False):
        if not isinstance(query, str):
            raise TypeError("Query must be a string")
        return query.upper() if uppercase else query.lower()
