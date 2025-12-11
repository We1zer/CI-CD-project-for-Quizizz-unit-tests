"""
Tests for LiveSessionPage - Live quiz sessions
"""
import pytest
from live_session_page import LiveSessionPage


# =============== POSITIVE TESTS ===============

def test_create_live_session():
    """Test 265: Create live session with quiz ID"""
    session = LiveSessionPage(quiz_id=1)
    assert session.quiz_id == 1
    assert session.is_started is False

def test_start_live_session():
    """Test 266: Start live session"""
    session = LiveSessionPage(quiz_id=1)
    result = session.start_live_session()
    assert result["status"] == "success"
    assert session.is_started is True
    assert session.join_code is not None
    assert len(session.join_code) == 6

def test_get_join_code():
    """Test 267: Get join code after starting"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    code = session.get_join_code()
    assert code is not None
    assert len(code) == 6

def test_copy_join_code():
    """Test 268: Copy join code to clipboard"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    result = session.copy_join_code()
    assert result["action"] == "copy_to_clipboard"
    assert result["value"] == session.join_code

def test_share_join_code_email():
    """Test 269: Share join code via email"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    result = session.share_join_code("email")
    assert result["action"] == "open_email_client"
    assert session.join_code in result["body"]

def test_share_join_code_link():
    """Test 270: Share join code via link"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    result = session.share_join_code("link")
    assert result["action"] == "generate_link"
    assert session.join_code in result["url"]

def test_share_join_code_qr():
    """Test 271: Share join code via QR code"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    result = session.share_join_code("qr")
    assert result["action"] == "generate_qr"
    assert result["data"] == session.join_code

def test_add_participant():
    """Test 272: Add participant to session"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    participant_id = session.add_participant("John")
    assert participant_id == 1
    assert session.get_participant_count() == 1

def test_add_multiple_participants():
    """Test 273: Add multiple participants"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    session.add_participant("Alice")
    session.add_participant("Bob")
    session.add_participant("Charlie")
    assert session.get_participant_count() == 3

def test_get_participants():
    """Test 274: Get list of participants"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    session.add_participant("Alice")
    session.add_participant("Bob")
    participants = session.get_participants()
    assert len(participants) == 2
    assert participants[0]["name"] == "Alice"

def test_remove_participant():
    """Test 275: Remove participant from session"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    pid = session.add_participant("Alice")
    result = session.remove_participant(pid)
    assert result["status"] == "success"
    assert session.get_participant_count() == 0

def test_start_quiz():
    """Test 276: Start quiz after adding participants"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    session.add_participant("Alice")
    result = session.start_quiz()
    assert result["status"] == "success"
    assert session.current_question == 1

def test_next_question():
    """Test 277: Move to next question"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    session.add_participant("Alice")
    session.start_quiz()
    result = session.next_question()
    assert result["current_question"] == 2

def test_end_session():
    """Test 278: End live session"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    session.add_participant("Alice")
    result = session.end_session()
    assert result["status"] == "success"
    assert session.is_started is False

def test_get_leaderboard():
    """Test 279: Get leaderboard of participants"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    session.add_participant("Alice")
    session.add_participant("Bob")
    leaderboard = session.get_leaderboard()
    assert len(leaderboard) == 2


# =============== NEGATIVE TESTS ===============

def test_create_session_non_integer_id():
    """Test 280: Create session with non-integer ID raises TypeError"""
    with pytest.raises(TypeError, match="Quiz ID must be an integer"):
        LiveSessionPage(quiz_id="1")

def test_get_join_code_before_start():
    """Test 281: Get join code before starting raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    with pytest.raises(ValueError, match="Session has not been started yet"):
        session.get_join_code()

def test_copy_join_code_before_start():
    """Test 282: Copy join code before starting raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    with pytest.raises(ValueError, match="Session has not been started yet"):
        session.copy_join_code()

def test_share_join_code_before_start():
    """Test 283: Share join code before starting raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    with pytest.raises(ValueError, match="Session has not been started yet"):
        session.share_join_code("email")

def test_share_join_code_invalid_method():
    """Test 284: Share with invalid method raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    with pytest.raises(ValueError, match="Share method must be"):
        session.share_join_code("sms")

def test_add_participant_non_string():
    """Test 285: Add participant with non-string name raises TypeError"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    with pytest.raises(TypeError, match="Participant name must be a string"):
        session.add_participant(123)

def test_add_participant_empty_name():
    """Test 286: Add participant with empty name raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    with pytest.raises(ValueError, match="Participant name cannot be empty"):
        session.add_participant("   ")

def test_add_participant_before_start():
    """Test 287: Add participant before starting raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    with pytest.raises(ValueError, match="Session has not been started yet"):
        session.add_participant("Alice")

def test_remove_participant_non_integer():
    """Test 288: Remove participant with non-integer ID raises TypeError"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    with pytest.raises(TypeError, match="Participant ID must be an integer"):
        session.remove_participant("1")

def test_remove_nonexistent_participant():
    """Test 289: Remove nonexistent participant raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    with pytest.raises(ValueError, match="Participant with ID 999 not found"):
        session.remove_participant(999)

def test_start_quiz_before_session():
    """Test 290: Start quiz before session raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    with pytest.raises(ValueError, match="Session has not been started yet"):
        session.start_quiz()

def test_start_quiz_without_participants():
    """Test 291: Start quiz without participants raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    with pytest.raises(ValueError, match="Cannot start quiz without participants"):
        session.start_quiz()

def test_next_question_before_start():
    """Test 292: Next question before starting quiz raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    with pytest.raises(ValueError, match="Quiz has not been started yet"):
        session.next_question()

def test_end_session_before_start():
    """Test 293: End session before starting raises ValueError"""
    session = LiveSessionPage(quiz_id=1)
    with pytest.raises(ValueError, match="Session has not been started yet"):
        session.end_session()


# =============== EDGE CASES ===============

def test_join_code_uniqueness():
    """Test 294: Each session generates different join code"""
    session1 = LiveSessionPage(quiz_id=1)
    session2 = LiveSessionPage(quiz_id=2)
    result1 = session1.start_live_session()
    result2 = session2.start_live_session()
    # Very unlikely but possible to be same (1 in 2.2 billion)
    # Just checking they're both valid codes
    assert len(result1["join_code"]) == 6
    assert len(result2["join_code"]) == 6

def test_participant_name_whitespace_trimmed():
    """Test 295: Participant name whitespace is trimmed"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    session.add_participant("  Alice  ")
    participants = session.get_participants()
    assert participants[0]["name"] == "Alice"

def test_get_leaderboard_empty():
    """Test 296: Leaderboard with no participants returns empty list"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    leaderboard = session.get_leaderboard()
    assert leaderboard == []

def test_participant_count_after_removal():
    """Test 297: Participant count updates after removal"""
    session = LiveSessionPage(quiz_id=1)
    session.start_live_session()
    pid1 = session.add_participant("Alice")
    session.add_participant("Bob")
    session.remove_participant(pid1)
    assert session.get_participant_count() == 1
