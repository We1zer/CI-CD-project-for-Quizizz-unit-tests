"""
Tests for HomeworkAssignPage - Homework assignments
"""
import pytest
from homework_assign_page import HomeworkAssignPage
from datetime import datetime, timedelta


# =============== POSITIVE TESTS ===============

def test_create_homework_page():
    """Test 298: Create homework assignment page"""
    page = HomeworkAssignPage(quiz_id=1)
    assert page.quiz_id == 1
    assert page.is_assigned is False

def test_set_homework_name():
    """Test 299: Set homework name"""
    page = HomeworkAssignPage(quiz_id=1)
    result = page.set_homework_name("Math Homework #1")
    assert result is True
    assert page.homework_name == "Math Homework #1"

def test_set_due_date():
    """Test 300: Set valid due date"""
    page = HomeworkAssignPage(quiz_id=1)
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    result = page.set_due_date(future_date)
    assert result is True
    assert page.due_date == future_date

def test_add_class():
    """Test 301: Add a class to assignment"""
    page = HomeworkAssignPage(quiz_id=1)
    result = page.add_class("Class 5A")
    assert result is True
    assert "Class 5A" in page.selected_classes

def test_add_multiple_classes():
    """Test 302: Add multiple classes"""
    page = HomeworkAssignPage(quiz_id=1)
    page.add_class("Class 5A")
    page.add_class("Class 5B")
    page.add_class("Class 6A")
    assert len(page.selected_classes) == 3

def test_remove_class():
    """Test 303: Remove class from assignment"""
    page = HomeworkAssignPage(quiz_id=1)
    page.add_class("Class 5A")
    result = page.remove_class("Class 5A")
    assert result is True
    assert "Class 5A" not in page.selected_classes

def test_get_selected_classes():
    """Test 304: Get list of selected classes"""
    page = HomeworkAssignPage(quiz_id=1)
    page.add_class("Class 5A")
    page.add_class("Class 5B")
    classes = page.get_selected_classes()
    assert len(classes) == 2
    assert "Class 5A" in classes

def test_set_instructions():
    """Test 305: Set homework instructions"""
    page = HomeworkAssignPage(quiz_id=1)
    result = page.set_instructions("Complete all questions by Friday")
    assert result is True
    assert page.instructions == "Complete all questions by Friday"

def test_assign_homework():
    """Test 306: Assign homework successfully"""
    page = HomeworkAssignPage(quiz_id=1)
    page.set_homework_name("Homework 1")
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    page.set_due_date(future_date)
    page.add_class("Class 5A")
    result = page.assign_homework()
    assert result["status"] == "success"
    assert page.is_assigned is True

def test_cancel_assignment():
    """Test 307: Cancel homework assignment"""
    page = HomeworkAssignPage(quiz_id=1)
    page.set_homework_name("Homework 1")
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    page.set_due_date(future_date)
    page.add_class("Class 5A")
    page.assign_homework()
    result = page.cancel_assignment()
    assert result["status"] == "success"
    assert page.is_assigned is False

def test_get_assignment_summary():
    """Test 308: Get assignment summary"""
    page = HomeworkAssignPage(quiz_id=1)
    page.set_homework_name("Homework 1")
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    page.set_due_date(future_date)
    page.add_class("Class 5A")
    summary = page.get_assignment_summary()
    assert summary["homework_name"] == "Homework 1"
    assert summary["quiz_id"] == 1
    assert len(summary["classes"]) == 1


# =============== NEGATIVE TESTS ===============

def test_create_homework_non_integer_id():
    """Test 309: Create with non-integer quiz ID raises TypeError"""
    with pytest.raises(TypeError, match="Quiz ID must be an integer"):
        HomeworkAssignPage(quiz_id="1")

def test_set_homework_name_non_string():
    """Test 310: Set homework name with non-string raises TypeError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(TypeError, match="Homework name must be a string"):
        page.set_homework_name(123)

def test_set_homework_name_empty():
    """Test 311: Empty homework name raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(ValueError, match="Homework name cannot be empty"):
        page.set_homework_name("   ")

def test_set_due_date_non_string():
    """Test 312: Set due date with non-string raises TypeError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(TypeError, match="Due date must be a string"):
        page.set_due_date(20240115)

def test_set_due_date_invalid_format():
    """Test 313: Invalid date format raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(ValueError, match="Invalid date format"):
        page.set_due_date("15-01-2024")

def test_set_due_date_in_past():
    """Test 314: Due date in past raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    with pytest.raises(ValueError, match="Due date must be in the future"):
        page.set_due_date(past_date)

def test_add_class_non_string():
    """Test 315: Add class with non-string raises TypeError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(TypeError, match="Class name must be a string"):
        page.add_class(5)

def test_add_class_empty():
    """Test 316: Empty class name raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(ValueError, match="Class name cannot be empty"):
        page.add_class("")

def test_add_duplicate_class():
    """Test 317: Adding duplicate class raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    page.add_class("Class 5A")
    with pytest.raises(ValueError, match="Class 'Class 5A' already added"):
        page.add_class("Class 5A")

def test_remove_nonexistent_class():
    """Test 318: Remove nonexistent class raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(ValueError, match="Class 'Class 5A' not found"):
        page.remove_class("Class 5A")

def test_remove_class_non_string():
    """Test 319: Remove class with non-string raises TypeError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(TypeError, match="Class name must be a string"):
        page.remove_class(123)

def test_set_instructions_non_string():
    """Test 320: Set instructions with non-string raises TypeError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(TypeError, match="Instructions must be a string"):
        page.set_instructions(123)

def test_assign_homework_without_name():
    """Test 321: Assign without homework name raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    page.set_due_date(future_date)
    page.add_class("Class 5A")
    with pytest.raises(ValueError, match="Homework name must be set"):
        page.assign_homework()

def test_assign_homework_without_due_date():
    """Test 322: Assign without due date raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    page.set_homework_name("Homework 1")
    page.add_class("Class 5A")
    with pytest.raises(ValueError, match="Due date must be set"):
        page.assign_homework()

def test_assign_homework_without_classes():
    """Test 323: Assign without classes raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    page.set_homework_name("Homework 1")
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    page.set_due_date(future_date)
    with pytest.raises(ValueError, match="At least one class must be selected"):
        page.assign_homework()

def test_cancel_assignment_before_assigning():
    """Test 324: Cancel assignment before assigning raises ValueError"""
    page = HomeworkAssignPage(quiz_id=1)
    with pytest.raises(ValueError, match="No homework has been assigned yet"):
        page.cancel_assignment()


# =============== EDGE CASES ===============

def test_homework_name_whitespace_trimmed():
    """Test 325: Homework name whitespace is trimmed"""
    page = HomeworkAssignPage(quiz_id=1)
    page.set_homework_name("  Homework 1  ")
    assert page.homework_name == "Homework 1"

def test_class_name_whitespace_trimmed():
    """Test 326: Class name whitespace is trimmed"""
    page = HomeworkAssignPage(quiz_id=1)
    page.add_class("  Class 5A  ")
    assert "Class 5A" in page.selected_classes

def test_empty_instructions():
    """Test 327: Empty instructions allowed"""
    page = HomeworkAssignPage(quiz_id=1)
    result = page.set_instructions("")
    assert result is True
    assert page.instructions == ""

def test_assignment_summary_before_assignment():
    """Test 328: Summary shows is_assigned as False before assignment"""
    page = HomeworkAssignPage(quiz_id=1)
    page.set_homework_name("Homework 1")
    summary = page.get_assignment_summary()
    assert summary["is_assigned"] is False
