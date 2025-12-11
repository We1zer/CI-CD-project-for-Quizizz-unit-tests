
class CartPage:
    """Quizizz library - save favorite quizzes, organize collections"""
    def __init__(self):
        self.saved_quizzes = []
        self.quiz_plays = {}
        self.total_questions = 0

    def add_quiz(self, quiz_id, plays=0, questions=10):
        """Add quiz to library"""
        if quiz_id <= 0:
            raise ValueError("Invalid quiz ID")
        if plays < 0:
            raise ValueError("Plays cannot be negative")
        if questions <= 0:
            raise ValueError("Questions must be positive")
        
        self.saved_quizzes.append(quiz_id)
        self.quiz_plays[quiz_id] = self.quiz_plays.get(quiz_id, 0) + plays
        self.total_questions += questions
        return self.saved_quizzes

    def remove_quiz(self, quiz_id):
        """Remove quiz from library"""
        if quiz_id not in self.saved_quizzes:
            raise ValueError("Quiz not in library")
        self.saved_quizzes.remove(quiz_id)
        if quiz_id in self.quiz_plays:
            del self.quiz_plays[quiz_id]
        return self.saved_quizzes

    def get_quizzes(self):
        """Get all saved quizzes"""
        return list(self.saved_quizzes)
    
    def get_quiz_count(self):
        return len(self.saved_quizzes)
    
    def get_plays(self, quiz_id):
        """Get number of plays for a quiz"""
        return self.quiz_plays.get(quiz_id, 0)
    
    def update_plays(self, quiz_id, plays):
        """Update play count for a quiz"""
        if quiz_id not in self.saved_quizzes:
            raise ValueError("Quiz not in library")
        if plays < 0:
            raise ValueError("Plays cannot be negative")
        self.quiz_plays[quiz_id] = plays
        return self.quiz_plays[quiz_id]
    
    def clear_library(self):
        """Clear all saved quizzes"""
        self.saved_quizzes = []
        self.quiz_plays = {}
        self.total_questions = 0
        return self.saved_quizzes
    
    def get_total_questions(self):
        return self.total_questions
    
    def is_empty(self):
        return len(self.saved_quizzes) == 0
    
    def has_quiz(self, quiz_id):
        return quiz_id in self.saved_quizzes
