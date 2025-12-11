"""
QuizEditorPage - Create and edit quiz questions with multimedia, timer, answers
"""

class QuizEditorPage:
    def __init__(self, quiz_id=None):
        self.quiz_id = quiz_id
        self.quiz_name = ""
        self.questions = []
        self.is_saved = False
        self.current_question_index = -1
    
    def set_quiz_name(self, name):
        """Set the quiz name"""
        if not isinstance(name, str):
            raise TypeError("Quiz name must be a string")
        if not name.strip():
            raise ValueError("Quiz name cannot be empty")
        self.quiz_name = name.strip()
        return True
    
    def add_question(self, question_text):
        """Add a new question to the quiz"""
        if not isinstance(question_text, str):
            raise TypeError("Question text must be a string")
        if not question_text.strip():
            raise ValueError("Question text cannot be empty")
        
        question = {
            "id": len(self.questions) + 1,
            "text": question_text.strip(),
            "answers": [],
            "correct_answer_ids": [],
            "media": None,
            "timer": 30
        }
        self.questions.append(question)
        self.current_question_index = len(self.questions) - 1
        return question["id"]
    
    def edit_question_text(self, question_id, new_text):
        """Edit the text of an existing question"""
        if not isinstance(question_id, int):
            raise TypeError("Question ID must be an integer")
        if not isinstance(new_text, str):
            raise TypeError("New text must be a string")
        if not new_text.strip():
            raise ValueError("Question text cannot be empty")
        
        question = self._get_question_by_id(question_id)
        if question is None:
            raise ValueError(f"Question with ID {question_id} not found")
        
        question["text"] = new_text.strip()
        return True
    
    def delete_question(self, question_id):
        """Delete a question from the quiz"""
        if not isinstance(question_id, int):
            raise TypeError("Question ID must be an integer")
        
        question = self._get_question_by_id(question_id)
        if question is None:
            raise ValueError(f"Question with ID {question_id} not found")
        
        self.questions = [q for q in self.questions if q["id"] != question_id]
        return {"status": "success", "message": f"Question {question_id} deleted"}
    
    def add_answer(self, question_id, answer_text, is_correct=False):
        """Add an answer option to a question"""
        if not isinstance(question_id, int):
            raise TypeError("Question ID must be an integer")
        if not isinstance(answer_text, str):
            raise TypeError("Answer text must be a string")
        if not answer_text.strip():
            raise ValueError("Answer text cannot be empty")
        
        question = self._get_question_by_id(question_id)
        if question is None:
            raise ValueError(f"Question with ID {question_id} not found")
        
        answer_id = len(question["answers"]) + 1
        question["answers"].append({
            "id": answer_id,
            "text": answer_text.strip()
        })
        
        if is_correct:
            question["correct_answer_ids"].append(answer_id)
        
        return answer_id
    
    def set_correct_answer(self, question_id, answer_id):
        """Mark an answer as correct"""
        if not isinstance(question_id, int) or not isinstance(answer_id, int):
            raise TypeError("IDs must be integers")
        
        question = self._get_question_by_id(question_id)
        if question is None:
            raise ValueError(f"Question with ID {question_id} not found")
        
        # Check if answer exists
        answer_exists = any(a["id"] == answer_id for a in question["answers"])
        if not answer_exists:
            raise ValueError(f"Answer with ID {answer_id} not found")
        
        if answer_id not in question["correct_answer_ids"]:
            question["correct_answer_ids"].append(answer_id)
        return True
    
    def set_incorrect_answer(self, question_id, answer_id):
        """Mark an answer as incorrect"""
        if not isinstance(question_id, int) or not isinstance(answer_id, int):
            raise TypeError("IDs must be integers")
        
        question = self._get_question_by_id(question_id)
        if question is None:
            raise ValueError(f"Question with ID {question_id} not found")
        
        if answer_id in question["correct_answer_ids"]:
            question["correct_answer_ids"].remove(answer_id)
        return True
    
    def add_media(self, question_id, media_url, media_type):
        """Add multimedia (image/video) to a question"""
        if not isinstance(question_id, int):
            raise TypeError("Question ID must be an integer")
        if not isinstance(media_url, str):
            raise TypeError("Media URL must be a string")
        if media_type not in ["image", "video"]:
            raise ValueError("Media type must be 'image' or 'video'")
        
        question = self._get_question_by_id(question_id)
        if question is None:
            raise ValueError(f"Question with ID {question_id} not found")
        
        question["media"] = {
            "url": media_url,
            "type": media_type
        }
        return True
    
    def remove_media(self, question_id):
        """Remove multimedia from a question"""
        if not isinstance(question_id, int):
            raise TypeError("Question ID must be an integer")
        
        question = self._get_question_by_id(question_id)
        if question is None:
            raise ValueError(f"Question with ID {question_id} not found")
        
        question["media"] = None
        return True
    
    def set_timer(self, question_id, seconds):
        """Set timer duration for a question"""
        if not isinstance(question_id, int):
            raise TypeError("Question ID must be an integer")
        if not isinstance(seconds, int):
            raise TypeError("Timer must be an integer")
        if seconds < 5 or seconds > 300:
            raise ValueError("Timer must be between 5 and 300 seconds")
        
        question = self._get_question_by_id(question_id)
        if question is None:
            raise ValueError(f"Question with ID {question_id} not found")
        
        question["timer"] = seconds
        return True
    
    def save_quiz(self):
        """Save the quiz"""
        if not self.quiz_name:
            raise ValueError("Quiz name must be set before saving")
        if len(self.questions) == 0:
            raise ValueError("Quiz must have at least one question")
        
        # Check that all questions have at least one correct answer
        for q in self.questions:
            if len(q["correct_answer_ids"]) == 0:
                raise ValueError(f"Question '{q['text']}' must have at least one correct answer")
            if len(q["answers"]) < 2:
                raise ValueError(f"Question '{q['text']}' must have at least 2 answers")
        
        self.is_saved = True
        return {
            "status": "success",
            "quiz_id": self.quiz_id or len(self.questions) * 100,
            "message": "Quiz saved successfully"
        }
    
    def get_question_count(self):
        """Get total number of questions"""
        return len(self.questions)
    
    def get_question(self, question_id):
        """Get a specific question by ID"""
        return self._get_question_by_id(question_id)
    
    def _get_question_by_id(self, question_id):
        """Internal method to find question by ID"""
        for question in self.questions:
            if question["id"] == question_id:
                return question
        return None
