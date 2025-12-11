"""
LiveSessionPage - Live quiz session with join codes and participant tracking
"""

class LiveSessionPage:
    def __init__(self, quiz_id):
        if not isinstance(quiz_id, int):
            raise TypeError("Quiz ID must be an integer")
        self.quiz_id = quiz_id
        self.join_code = None
        self.is_started = False
        self.participants = []
        self.current_question = 0
    
    def start_live_session(self):
        """Start a live quiz session"""
        import random
        import string
        
        # Generate random 6-character join code
        self.join_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.is_started = True
        return {
            "status": "success",
            "join_code": self.join_code,
            "message": "Live session started"
        }
    
    def get_join_code(self):
        """Get the session join code"""
        if not self.is_started:
            raise ValueError("Session has not been started yet")
        return self.join_code
    
    def copy_join_code(self):
        """Copy join code to clipboard"""
        if not self.is_started:
            raise ValueError("Session has not been started yet")
        return {"action": "copy_to_clipboard", "value": self.join_code}
    
    def share_join_code(self, method):
        """Share join code via email, link, or QR code"""
        if not self.is_started:
            raise ValueError("Session has not been started yet")
        if method not in ["email", "link", "qr"]:
            raise ValueError("Share method must be 'email', 'link', or 'qr'")
        
        if method == "email":
            return {"action": "open_email_client", "body": f"Join my quiz with code: {self.join_code}"}
        elif method == "link":
            return {"action": "generate_link", "url": f"https://quizizz.com/join?code={self.join_code}"}
        else:  # qr
            return {"action": "generate_qr", "data": self.join_code}
    
    def add_participant(self, name):
        """Add a participant to the session"""
        if not isinstance(name, str):
            raise TypeError("Participant name must be a string")
        if not name.strip():
            raise ValueError("Participant name cannot be empty")
        if not self.is_started:
            raise ValueError("Session has not been started yet")
        
        participant = {
            "id": len(self.participants) + 1,
            "name": name.strip(),
            "joined_at": "2024-01-15 10:00:00",
            "score": 0
        }
        self.participants.append(participant)
        return participant["id"]
    
    def get_participant_count(self):
        """Get number of participants"""
        return len(self.participants)
    
    def get_participants(self):
        """Get list of all participants"""
        return self.participants.copy()
    
    def remove_participant(self, participant_id):
        """Remove a participant from session"""
        if not isinstance(participant_id, int):
            raise TypeError("Participant ID must be an integer")
        
        participant = self._get_participant_by_id(participant_id)
        if participant is None:
            raise ValueError(f"Participant with ID {participant_id} not found")
        
        self.participants = [p for p in self.participants if p["id"] != participant_id]
        return {"status": "success", "message": f"Participant {participant_id} removed"}
    
    def start_quiz(self):
        """Start the quiz questions"""
        if not self.is_started:
            raise ValueError("Session has not been started yet")
        if len(self.participants) == 0:
            raise ValueError("Cannot start quiz without participants")
        
        self.current_question = 1
        return {
            "status": "success",
            "message": "Quiz started",
            "current_question": self.current_question
        }
    
    def next_question(self):
        """Move to next question"""
        if self.current_question == 0:
            raise ValueError("Quiz has not been started yet")
        
        self.current_question += 1
        return {"current_question": self.current_question}
    
    def end_session(self):
        """End the live session"""
        if not self.is_started:
            raise ValueError("Session has not been started yet")
        
        self.is_started = False
        return {
            "status": "success",
            "total_participants": len(self.participants),
            "message": "Session ended"
        }
    
    def get_leaderboard(self):
        """Get current leaderboard"""
        if len(self.participants) == 0:
            return []
        
        sorted_participants = sorted(self.participants, key=lambda p: p["score"], reverse=True)
        return sorted_participants
    
    def _get_participant_by_id(self, participant_id):
        """Internal method to find participant by ID"""
        for participant in self.participants:
            if participant["id"] == participant_id:
                return participant
        return None
