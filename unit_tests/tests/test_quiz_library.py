import pytest
from quiz_library_page import QuizLibraryPage


# =============== POSITIVE TESTS ===============

def test_add_quiz_basic():
    """Test 1: Add a quiz to library"""
    page = QuizLibraryPage()
    result = page.add_quiz(1)
    assert 1 in result

def test_add_quiz_with_plays():
    """Test 2: Add quiz with play count"""
    page = QuizLibraryPage()
    result = page.add_quiz(1, plays=50)
    assert page.get_plays(1) == 50

def test_add_quiz_with_questions():
    """Test 3: Add quiz with question count"""
    page = QuizLibraryPage()
    page.add_quiz(1, questions=20)
    assert page.get_total_questions() == 20

def test_remove_quiz():
    """Test 4: Remove quiz from library"""
    page = QuizLibraryPage()
    page.add_quiz(1)
    result = page.remove_quiz(1)
    assert 1 not in result

def test_get_quizzes_empty():
    """Test 5: Get quizzes from empty library"""
    page = QuizLibraryPage()
    result = page.get_quizzes()
    assert len(result) == 0

def test_get_quiz_count():
    """Test 6: Get count of saved quizzes"""
    page = QuizLibraryPage()
    page.add_quiz(1)
    page.add_quiz(2)
    assert page.get_quiz_count() == 2

def test_update_plays():
    """Test 7: Update play count for a quiz"""
    page = QuizLibraryPage()
    page.add_quiz(1, plays=10)
    page.update_plays(1, 20)
    assert page.get_plays(1) == 20

def test_clear_library():
    """Test 8: Clear all saved quizzes"""
    page = QuizLibraryPage()
    page.add_quiz(1)
    page.add_quiz(2)
    result = page.clear_library()
    assert len(result) == 0

def test_is_empty_true():
    """Test 9: Library is empty returns True"""
    page = QuizLibraryPage()
    assert page.is_empty() is True

def test_is_empty_false():
    """Test 10: Library with quizzes returns False"""
    page = QuizLibraryPage()
    page.add_quiz(1)
    assert page.is_empty() is False

def test_has_quiz_true():
    """Test 11: Library contains quiz"""
    page = QuizLibraryPage()
    page.add_quiz(1)
    assert page.has_quiz(1) is True

def test_has_quiz_false():
    """Test 12: Library doesn't contain quiz"""
    page = QuizLibraryPage()
    assert page.has_quiz(99) is False

def test_get_plays_nonexistent():
    """Test 13: Get plays for non-existent quiz returns 0"""
    page = QuizLibraryPage()
    assert page.get_plays(99) == 0

def test_multiple_same_quizzes():
    """Test 14: Adding same quiz multiple times accumulates plays"""
    page = QuizLibraryPage()
    page.add_quiz(1, plays=10)
    page.add_quiz(1, plays=5)
    assert page.get_plays(1) == 15

def test_total_questions_multiple_quizzes():
    """Test 15: Total questions across multiple quizzes"""
    page = QuizLibraryPage()
    page.add_quiz(1, questions=10)
    page.add_quiz(2, questions=15)
    assert page.get_total_questions() == 25

def test_clear_library_resets_questions():
    """Test 16: Clear library resets total questions"""
    page = QuizLibraryPage()
    page.add_quiz(1, questions=20)
    page.clear_library()
    assert page.get_total_questions() == 0

def test_get_quizzes_returns_copy():
    """Test 17: get_quizzes returns a copy"""
    page = QuizLibraryPage()
    page.add_quiz(1)
    quizzes = page.get_quizzes()
    quizzes.append(999)
    assert 999 not in page.get_quizzes()


# =============== NEGATIVE TESTS ===============

def test_add_invalid_quiz_id_zero():
    """Test 18: Add quiz with ID 0 raises error"""
    page = QuizLibraryPage()
    with pytest.raises(ValueError, match="Invalid quiz ID"):
        page.add_quiz(0)

def test_add_invalid_quiz_id_negative():
    """Test 19: Add quiz with negative ID raises error"""
    page = QuizLibraryPage()
    with pytest.raises(ValueError, match="Invalid quiz ID"):
        page.add_quiz(-1)

def test_add_quiz_negative_plays():
    """Test 20: Add quiz with negative plays raises error"""
    page = QuizLibraryPage()
    with pytest.raises(ValueError, match="Plays cannot be negative"):
        page.add_quiz(1, plays=-5)

def test_add_quiz_zero_questions():
    """Test 21: Add quiz with 0 questions raises error"""
    page = QuizLibraryPage()
    with pytest.raises(ValueError, match="Questions must be positive"):
        page.add_quiz(1, questions=0)

def test_add_quiz_negative_questions():
    """Test 22: Add quiz with negative questions raises error"""
    page = QuizLibraryPage()
    with pytest.raises(ValueError, match="Questions must be positive"):
        page.add_quiz(1, questions=-10)

def test_remove_nonexistent_quiz():
    """Test 23: Remove non-existent quiz raises error"""
    page = QuizLibraryPage()
    with pytest.raises(ValueError, match="Quiz not in library"):
        page.remove_quiz(99)

def test_update_plays_nonexistent_quiz():
    """Test 24: Update plays for non-existent quiz raises error"""
    page = QuizLibraryPage()
    with pytest.raises(ValueError, match="Quiz not in library"):
        page.update_plays(99, 10)

def test_update_plays_negative():
    """Test 25: Update plays with negative value raises error"""
    page = QuizLibraryPage()
    page.add_quiz(1)
    with pytest.raises(ValueError, match="Plays cannot be negative"):
        page.update_plays(1, -5)


# =============== EDGE CASE TESTS ===============

def test_add_quiz_with_zero_plays():
    """Test 26: Add quiz with 0 plays is valid"""
    page = QuizLibraryPage()
    page.add_quiz(1, plays=0)
    assert page.get_plays(1) == 0
