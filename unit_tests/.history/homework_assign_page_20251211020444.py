"""
HomeworkAssignPage - Assign homework with due dates and class selection
"""
from datetime import datetime

class HomeworkAssignPage:
    def __init__(self, quiz_id):
        if not isinstance(quiz_id, int):
            raise TypeError("Quiz ID must be an integer")
        self.quiz_id = quiz_id
        self.homework_name = ""
        self.due_date = None
        self.selected_classes = []
        self.instructions = ""
        self.is_assigned = False
    
    def set_homework_name(self, name):
        """Set homework assignment name"""
        if not isinstance(name, str):
            raise TypeError("Homework name must be a string")
        if not name.strip():
            raise ValueError("Homework name cannot be empty")
        self.homework_name = name.strip()
        return True
    
    def set_due_date(self, date_string):
        """Set homework due date (format: YYYY-MM-DD)"""
        if not isinstance(date_string, str):
            raise TypeError("Due date must be a string")
        
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
        # Check if date is in the future
        if date_obj < datetime.now():
            raise ValueError("Due date must be in the future")
        
        self.due_date = date_string
        return True
    
    def add_class(self, class_name):
        """Add a class to receive the homework"""
        if not isinstance(class_name, str):
            raise TypeError("Class name must be a string")
        if not class_name.strip():
            raise ValueError("Class name cannot be empty")
        
        if class_name in self.selected_classes:
            raise ValueError(f"Class '{class_name}' already added")
        
        self.selected_classes.append(class_name.strip())
        return True
    
    def remove_class(self, class_name):
        """Remove a class from homework assignment"""
        if not isinstance(class_name, str):
            raise TypeError("Class name must be a string")
        
        if class_name not in self.selected_classes:
            raise ValueError(f"Class '{class_name}' not found")
        
        self.selected_classes.remove(class_name)
        return True
    
    def get_selected_classes(self):
        """Get list of selected classes"""
        return self.selected_classes.copy()
    
    def set_instructions(self, text):
        """Set homework instructions"""
        if not isinstance(text, str):
            raise TypeError("Instructions must be a string")
        self.instructions = text.strip()
        return True
    
    def assign_homework(self):
        """Assign the homework"""
        if not self.homework_name:
            raise ValueError("Homework name must be set")
        if self.due_date is None:
            raise ValueError("Due date must be set")
        if len(self.selected_classes) == 0:
            raise ValueError("At least one class must be selected")
        
        self.is_assigned = True
        return {
            "status": "success",
            "homework_id": self.quiz_id * 10,
            "message": f"Homework assigned to {len(self.selected_classes)} class(es)",
            "due_date": self.due_date
        }
    
    def cancel_assignment(self):
        """Cancel homework assignment"""
        if not self.is_assigned:
            raise ValueError("No homework has been assigned yet")
        
        self.is_assigned = False
        return {"status": "success", "message": "Homework assignment cancelled"}
    
    def get_assignment_summary(self):
        """Get summary of homework assignment"""
        return {
            "homework_name": self.homework_name,
            "quiz_id": self.quiz_id,
            "due_date": self.due_date,
            "classes": self.selected_classes,
            "instructions": self.instructions,
            "is_assigned": self.is_assigned
        }
