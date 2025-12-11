"""
Tests for QuizEditorPage - Quiz creation and editing
"""
import pytest
from quiz_editor_page import QuizEditorPage


# =============== POSITIVE TESTS ===============

def test_set_quiz_name():
    """Test 224: Set quiz name"""
    editor = QuizEditorPage()
    result = editor.set_quiz_name("My Quiz")
    assert result is True
    assert editor.quiz_name == "My Quiz"

def test_add_question():
    """Test 225: Add a new question"""
    editor = QuizEditorPage()
    question_id = editor.add_question("What is 2+2?")
    assert question_id == 1
    assert editor.get_question_count() == 1

def test_add_multiple_questions():
    """Test 226: Add multiple questions"""
    editor = QuizEditorPage()
    editor.add_question("Question 1")
    editor.add_question("Question 2")
    editor.add_question("Question 3")
    assert editor.get_question_count() == 3

def test_edit_question_text():
    """Test 227: Edit question text"""
    editor = QuizEditorPage()
    qid = editor.add_question("Original text")
    result = editor.edit_question_text(qid, "Updated text")
    assert result is True
    question = editor.get_question(qid)
    assert question["text"] == "Updated text"

def test_delete_question():
    """Test 228: Delete a question"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question to delete")
    result = editor.delete_question(qid)
    assert result["status"] == "success"
    assert editor.get_question_count() == 0

def test_add_answer():
    """Test 229: Add answer to question"""
    editor = QuizEditorPage()
    qid = editor.add_question("What is 2+2?")
    answer_id = editor.add_answer(qid, "4", is_correct=True)
    assert answer_id == 1
    question = editor.get_question(qid)
    assert len(question["answers"]) == 1
    assert 1 in question["correct_answer_ids"]

def test_add_multiple_answers():
    """Test 230: Add multiple answers"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    editor.add_answer(qid, "Answer 1", is_correct=True)
    editor.add_answer(qid, "Answer 2", is_correct=False)
    editor.add_answer(qid, "Answer 3", is_correct=False)
    question = editor.get_question(qid)
    assert len(question["answers"]) == 3

def test_set_correct_answer():
    """Test 231: Mark answer as correct"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    aid = editor.add_answer(qid, "Answer")
    result = editor.set_correct_answer(qid, aid)
    assert result is True
    question = editor.get_question(qid)
    assert aid in question["correct_answer_ids"]

def test_set_incorrect_answer():
    """Test 232: Mark answer as incorrect"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    aid = editor.add_answer(qid, "Answer", is_correct=True)
    result = editor.set_incorrect_answer(qid, aid)
    assert result is True
    question = editor.get_question(qid)
    assert aid not in question["correct_answer_ids"]

def test_add_image_media():
    """Test 233: Add image to question"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    result = editor.add_media(qid, "https://example.com/image.jpg", "image")
    assert result is True
    question = editor.get_question(qid)
    assert question["media"]["type"] == "image"

def test_add_video_media():
    """Test 234: Add video to question"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    result = editor.add_media(qid, "https://youtube.com/watch?v=123", "video")
    assert result is True
    question = editor.get_question(qid)
    assert question["media"]["type"] == "video"

def test_remove_media():
    """Test 235: Remove media from question"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    editor.add_media(qid, "https://example.com/image.jpg", "image")
    result = editor.remove_media(qid)
    assert result is True
    question = editor.get_question(qid)
    assert question["media"] is None

def test_set_timer():
    """Test 236: Set question timer"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    result = editor.set_timer(qid, 60)
    assert result is True
    question = editor.get_question(qid)
    assert question["timer"] == 60

def test_save_quiz():
    """Test 237: Save complete quiz"""
    editor = QuizEditorPage()
    editor.set_quiz_name("Test Quiz")
    qid = editor.add_question("Question")
    editor.add_answer(qid, "Answer 1", is_correct=True)
    editor.add_answer(qid, "Answer 2")
    result = editor.save_quiz()
    assert result["status"] == "success"
    assert editor.is_saved is True

def test_get_question_by_id():
    """Test 238: Get specific question"""
    editor = QuizEditorPage()
    qid = editor.add_question("My Question")
    question = editor.get_question(qid)
    assert question is not None
    assert question["text"] == "My Question"


# =============== NEGATIVE TESTS ===============

def test_set_quiz_name_non_string():
    """Test 239: Set quiz name with non-string raises TypeError"""
    editor = QuizEditorPage()
    with pytest.raises(TypeError, match="Quiz name must be a string"):
        editor.set_quiz_name(123)

def test_set_quiz_name_empty():
    """Test 240: Empty quiz name raises ValueError"""
    editor = QuizEditorPage()
    with pytest.raises(ValueError, match="Quiz name cannot be empty"):
        editor.set_quiz_name("")

def test_add_question_non_string():
    """Test 241: Add question with non-string raises TypeError"""
    editor = QuizEditorPage()
    with pytest.raises(TypeError, match="Question text must be a string"):
        editor.add_question(None)

def test_add_question_empty():
    """Test 242: Empty question text raises ValueError"""
    editor = QuizEditorPage()
    with pytest.raises(ValueError, match="Question text cannot be empty"):
        editor.add_question("   ")

def test_edit_nonexistent_question():
    """Test 243: Edit nonexistent question raises ValueError"""
    editor = QuizEditorPage()
    with pytest.raises(ValueError, match="Question with ID 999 not found"):
        editor.edit_question_text(999, "New text")

def test_edit_question_non_integer_id():
    """Test 244: Edit question with non-integer ID raises TypeError"""
    editor = QuizEditorPage()
    with pytest.raises(TypeError, match="Question ID must be an integer"):
        editor.edit_question_text("1", "Text")

def test_edit_question_empty_text():
    """Test 245: Edit question with empty text raises ValueError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    with pytest.raises(ValueError, match="Question text cannot be empty"):
        editor.edit_question_text(qid, "")

def test_delete_nonexistent_question():
    """Test 246: Delete nonexistent question raises ValueError"""
    editor = QuizEditorPage()
    with pytest.raises(ValueError, match="Question with ID 999 not found"):
        editor.delete_question(999)

def test_add_answer_to_nonexistent_question():
    """Test 247: Add answer to nonexistent question raises ValueError"""
    editor = QuizEditorPage()
    with pytest.raises(ValueError, match="Question with ID 999 not found"):
        editor.add_answer(999, "Answer")

def test_add_answer_empty_text():
    """Test 248: Empty answer text raises ValueError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    with pytest.raises(ValueError, match="Answer text cannot be empty"):
        editor.add_answer(qid, "")

def test_set_correct_answer_nonexistent_question():
    """Test 249: Set correct answer for nonexistent question raises ValueError"""
    editor = QuizEditorPage()
    with pytest.raises(ValueError, match="Question with ID 999 not found"):
        editor.set_correct_answer(999, 1)

def test_set_correct_answer_nonexistent_answer():
    """Test 250: Set nonexistent answer as correct raises ValueError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    with pytest.raises(ValueError, match="Answer with ID 999 not found"):
        editor.set_correct_answer(qid, 999)

def test_add_media_invalid_type():
    """Test 251: Add media with invalid type raises ValueError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    with pytest.raises(ValueError, match="Media type must be 'image' or 'video'"):
        editor.add_media(qid, "url", "audio")

def test_add_media_non_string_url():
    """Test 252: Add media with non-string URL raises TypeError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    with pytest.raises(TypeError, match="Media URL must be a string"):
        editor.add_media(qid, 123, "image")

def test_set_timer_too_low():
    """Test 253: Timer below 5 seconds raises ValueError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    with pytest.raises(ValueError, match="Timer must be between 5 and 300 seconds"):
        editor.set_timer(qid, 3)

def test_set_timer_too_high():
    """Test 254: Timer above 300 seconds raises ValueError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    with pytest.raises(ValueError, match="Timer must be between 5 and 300 seconds"):
        editor.set_timer(qid, 400)

def test_set_timer_non_integer():
    """Test 255: Non-integer timer raises TypeError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    with pytest.raises(TypeError, match="Timer must be an integer"):
        editor.set_timer(qid, "60")

def test_save_quiz_without_name():
    """Test 256: Save quiz without name raises ValueError"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    editor.add_answer(qid, "Answer", is_correct=True)
    editor.add_answer(qid, "Answer 2")
    with pytest.raises(ValueError, match="Quiz name must be set before saving"):
        editor.save_quiz()

def test_save_quiz_without_questions():
    """Test 257: Save quiz without questions raises ValueError"""
    editor = QuizEditorPage()
    editor.set_quiz_name("Quiz")
    with pytest.raises(ValueError, match="Quiz must have at least one question"):
        editor.save_quiz()

def test_save_quiz_without_correct_answer():
    """Test 258: Save quiz with question missing correct answer raises ValueError"""
    editor = QuizEditorPage()
    editor.set_quiz_name("Quiz")
    qid = editor.add_question("Question")
    editor.add_answer(qid, "Answer 1")
    editor.add_answer(qid, "Answer 2")
    with pytest.raises(ValueError, match="must have at least one correct answer"):
        editor.save_quiz()

def test_save_quiz_with_insufficient_answers():
    """Test 259: Save quiz with less than 2 answers raises ValueError"""
    editor = QuizEditorPage()
    editor.set_quiz_name("Quiz")
    qid = editor.add_question("Question")
    editor.add_answer(qid, "Only one answer", is_correct=True)
    with pytest.raises(ValueError, match="must have at least 2 answers"):
        editor.save_quiz()


# =============== EDGE CASES ===============

def test_question_default_timer():
    """Test 260: New question has default 30s timer"""
    editor = QuizEditorPage()
    qid = editor.add_question("Question")
    question = editor.get_question(qid)
    assert question["timer"] == 30

def test_quiz_name_whitespace_trimmed():
    """Test 261: Quiz name whitespace is trimmed"""
    editor = QuizEditorPage()
    editor.set_quiz_name("  Quiz Name  ")
    assert editor.quiz_name == "Quiz Name"

def test_question_text_whitespace_trimmed():
    """Test 262: Question text whitespace is trimmed"""
    editor = QuizEditorPage()
    qid = editor.add_question("  Question?  ")
    question = editor.get_question(qid)
    assert question["text"] == "Question?"

def test_multiple_correct_answers():
    """Test 263: Question can have multiple correct answers"""
    editor = QuizEditorPage()
    qid = editor.add_question("Select all that apply")
    aid1 = editor.add_answer(qid, "Correct 1", is_correct=True)
    aid2 = editor.add_answer(qid, "Correct 2", is_correct=True)
    editor.add_answer(qid, "Incorrect")
    question = editor.get_question(qid)
    assert len(question["correct_answer_ids"]) == 2

def test_get_nonexistent_question_returns_none():
    """Test 264: Get nonexistent question returns None"""
    editor = QuizEditorPage()
    question = editor.get_question(999)
    assert question is None
