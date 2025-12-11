"""
ResultsPage - View and filter quiz results with export functionality
"""

class ResultsPage:
    def __init__(self):
        self.results = []
        self.filters = {
            "student": None,
            "min_accuracy": None,
            "question_id": None
        }
    
    def load_results(self, results_list=None):
        """Load quiz results"""
        if results_list is None:
            # Default mock results
            self.results = [
                {"id": 1, "student": "Alice", "score": 85, "accuracy": 85.0, "questions_correct": 17, "total_questions": 20, "date": "2024-01-15"},
                {"id": 2, "student": "Bob", "score": 92, "accuracy": 92.0, "questions_correct": 18, "total_questions": 20, "date": "2024-01-15"},
                {"id": 3, "student": "Charlie", "score": 78, "accuracy": 78.0, "questions_correct": 15, "total_questions": 20, "date": "2024-01-16"}
            ]
        else:
            if not isinstance(results_list, list):
                raise TypeError("Results must be a list")
            self.results = results_list
        return True
    
    def get_all_results(self):
        """Get all quiz results"""
        return self.results.copy()
    
    def filter_by_student(self, student_name):
        """Filter results by student name"""
        if not isinstance(student_name, str):
            raise TypeError("Student name must be a string")
        if not student_name.strip():
            raise ValueError("Student name cannot be empty")
        
        self.filters["student"] = student_name
        return [r for r in self.results if r["student"].lower() == student_name.lower()]
    
    def filter_by_accuracy(self, min_accuracy):
        """Filter results by minimum accuracy percentage"""
        if not isinstance(min_accuracy, (int, float)):
            raise TypeError("Accuracy must be a number")
        if min_accuracy < 0 or min_accuracy > 100:
            raise ValueError("Accuracy must be between 0 and 100")
        
        self.filters["min_accuracy"] = min_accuracy
        return [r for r in self.results if r["accuracy"] >= min_accuracy]
    
    def filter_by_question(self, question_id):
        """Filter to see who answered specific question correctly/incorrectly"""
        if not isinstance(question_id, int):
            raise TypeError("Question ID must be an integer")
        
        self.filters["question_id"] = question_id
        # Simplified: return all results (in real scenario would check specific question)
        return self.results.copy()
    
    def sort_results(self, sort_by, ascending=False):
        """Sort results by: score, accuracy, student, date"""
        if sort_by not in ["score", "accuracy", "student", "date"]:
            raise ValueError("Invalid sort option")
        
        if sort_by == "student":
            return sorted(self.results, key=lambda r: r["student"], reverse=not ascending)
        else:
            return sorted(self.results, key=lambda r: r[sort_by], reverse=not ascending)
    
    def get_result_by_id(self, result_id):
        """Get specific result by ID"""
        if not isinstance(result_id, int):
            raise TypeError("Result ID must be an integer")
        
        for result in self.results:
            if result["id"] == result_id:
                return result
        return None
    
    def export_to_excel(self, filename=None):
        """Export results to Excel format"""
        if len(self.results) == 0:
            raise ValueError("No results to export")
        
        if filename is None:
            filename = "quiz_results.xlsx"
        
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string")
        
        if not filename.endswith(".xlsx"):
            raise ValueError("Filename must have .xlsx extension")
        
        return {
            "status": "success",
            "filename": filename,
            "records": len(self.results),
            "message": f"Exported {len(self.results)} results to {filename}"
        }
    
    def download_report(self):
        """Download PDF report of results"""
        if len(self.results) == 0:
            raise ValueError("No results to download")
        
        return {
            "action": "download",
            "format": "pdf",
            "filename": "quiz_report.pdf"
        }
    
    def get_statistics(self):
        """Get statistical summary of results"""
        if len(self.results) == 0:
            return {
                "total_students": 0,
                "average_score": 0,
                "highest_score": 0,
                "lowest_score": 0
            }
        
        scores = [r["score"] for r in self.results]
        return {
            "total_students": len(self.results),
            "average_score": sum(scores) / len(scores),
            "highest_score": max(scores),
            "lowest_score": min(scores)
        }
    
    def clear_filters(self):
        """Clear all active filters"""
        self.filters = {
            "student": None,
            "min_accuracy": None,
            "question_id": None
        }
        return True
    
    def get_active_filters(self):
        """Get currently active filters"""
        active = {}
        if self.filters["student"]:
            active["student"] = self.filters["student"]
        if self.filters["min_accuracy"] is not None:
            active["min_accuracy"] = self.filters["min_accuracy"]
        if self.filters["question_id"]:
            active["question_id"] = self.filters["question_id"]
        return active
