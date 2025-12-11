"""
DashboardPage - Main quiz dashboard with search, filters, and creation
"""

class DashboardPage:
    def __init__(self):
        self.quizzes = []
        self.search_query = ""
        self.filters = {
            "subject": None,
            "grade": None,
            "sort_by": "date"
        }
        self.is_loaded = False
    
    def load_quizzes(self, quiz_list=None):
        """Load quizzes into dashboard"""
        if quiz_list is None:
            # Default mock quizzes
            self.quizzes = [
                {"id": 1, "name": "Math Quiz", "subject": "Math", "grade": 5, "questions": 10, "date": "2024-01-15"},
                {"id": 2, "name": "Science Test", "subject": "Science", "grade": 8, "questions": 15, "date": "2024-01-20"},
                {"id": 3, "name": "History Exam", "subject": "History", "grade": 10, "questions": 20, "date": "2024-01-10"}
            ]
        else:
            if not isinstance(quiz_list, list):
                raise TypeError("Quiz list must be a list")
            self.quizzes = quiz_list
        self.is_loaded = True
        return True
    
    def search_quiz(self, query):
        """Search quizzes by name"""
        if not isinstance(query, str):
            raise TypeError("Search query must be a string")
        
        self.search_query = query.strip()
        
        if not self.search_query:
            return self.quizzes
        
        results = [q for q in self.quizzes if self.search_query.lower() in q["name"].lower()]
        return results
    
    def filter_by_subject(self, subject):
        """Filter quizzes by subject"""
        if not isinstance(subject, str):
            raise TypeError("Subject must be a string")
        
        if subject not in ["Math", "Science", "History", "English", "Geography"]:
            raise ValueError("Invalid subject")
        
        self.filters["subject"] = subject
        return [q for q in self.quizzes if q["subject"] == subject]
    
    def filter_by_grade(self, grade):
        """Filter quizzes by grade level"""
        if not isinstance(grade, int):
            raise TypeError("Grade must be an integer")
        
        if grade < 1 or grade > 12:
            raise ValueError("Grade must be between 1 and 12")
        
        self.filters["grade"] = grade
        return [q for q in self.quizzes if q["grade"] == grade]
    
    def sort_quizzes(self, sort_by):
        """Sort quizzes by: date, name, questions"""
        if sort_by not in ["date", "name", "questions"]:
            raise ValueError("Invalid sort option")
        
        self.filters["sort_by"] = sort_by
        
        if sort_by == "date":
            return sorted(self.quizzes, key=lambda q: q["date"], reverse=True)
        elif sort_by == "name":
            return sorted(self.quizzes, key=lambda q: q["name"])
        else:  # questions
            return sorted(self.quizzes, key=lambda q: q["questions"], reverse=True)
    
    def click_create_quiz_button(self):
        """Click 'Create Quiz' button"""
        if not self.is_loaded:
            raise ValueError("Dashboard must be loaded first")
        return {"action": "navigate", "url": "/quiz/editor/new"}
    
    def get_quiz_count(self):
        """Get total number of quizzes"""
        return len(self.quizzes)
    
    def get_quiz_by_id(self, quiz_id):
        """Get specific quiz by ID"""
        if not isinstance(quiz_id, int):
            raise TypeError("Quiz ID must be an integer")
        
        for quiz in self.quizzes:
            if quiz["id"] == quiz_id:
                return quiz
        return None
    
    def open_quiz(self, quiz_id):
        """Open quiz for viewing/editing"""
        quiz = self.get_quiz_by_id(quiz_id)
        if quiz is None:
            raise ValueError(f"Quiz with ID {quiz_id} not found")
        return {"action": "navigate", "url": f"/quiz/editor/{quiz_id}", "quiz": quiz}
    
    def delete_quiz(self, quiz_id):
        """Delete a quiz from dashboard"""
        quiz = self.get_quiz_by_id(quiz_id)
        if quiz is None:
            raise ValueError(f"Quiz with ID {quiz_id} not found")
        
        self.quizzes = [q for q in self.quizzes if q["id"] != quiz_id]
        return {"status": "success", "message": f"Quiz {quiz_id} deleted"}
    
    def clear_filters(self):
        """Clear all active filters"""
        self.filters = {
            "subject": None,
            "grade": None,
            "sort_by": "date"
        }
        self.search_query = ""
        return True
    
    def get_active_filters(self):
        """Get currently active filters"""
        active = {}
        if self.filters["subject"]:
            active["subject"] = self.filters["subject"]
        if self.filters["grade"]:
            active["grade"] = self.filters["grade"]
        if self.search_query:
            active["search"] = self.search_query
        return active
