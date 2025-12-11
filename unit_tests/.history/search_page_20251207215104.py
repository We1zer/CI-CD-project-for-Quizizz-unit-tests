
class SearchPage:
    def __init__(self):
        self.last_query = None
        self.filters = {}
        self.results_cache = {}
    
    def search(self, query):
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Invalid query")
        self.last_query = query
        results = {"results": [query], "count": 1}
        self.results_cache[query] = results
        return results

    def sort_by_price(self, order):
        if order not in ("asc", "desc"):
            raise ValueError("Invalid sort order")
        return order
    
    def apply_filter(self, filter_name, value):
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
    
    def validate_price_range(self, min_price, max_price):
        if min_price < 0 or max_price < 0:
            raise ValueError("Prices cannot be negative")
        if min_price > max_price:
            raise ValueError("Min price cannot exceed max price")
        return {"min": min_price, "max": max_price}
    
    def format_query(self, query, uppercase=False):
        if not isinstance(query, str):
            raise TypeError("Query must be a string")
        return query.upper() if uppercase else query.lower()
