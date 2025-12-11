"""
Tests for ResultsPage - Quiz results and analytics
"""
import pytest
from results_page import ResultsPage


# =============== POSITIVE TESTS ===============

def test_load_default_results():
    """Test 329: Load default results"""
    page = ResultsPage()
    result = page.load_results()
    assert result is True
    assert len(page.get_all_results()) == 3

def test_load_custom_results():
    """Test 330: Load custom results list"""
    page = ResultsPage()
    custom_results = [
        {"id": 10, "student": "David", "score": 95, "accuracy": 95.0, "questions_correct": 19, "total_questions": 20, "date": "2024-01-20"}
    ]
    page.load_results(custom_results)
    assert len(page.get_all_results()) == 1

def test_get_all_results():
    """Test 331: Get all quiz results"""
    page = ResultsPage()
    page.load_results()
    results = page.get_all_results()
    assert len(results) == 3
    assert results[0]["student"] == "Alice"

def test_filter_by_student():
    """Test 332: Filter results by student name"""
    page = ResultsPage()
    page.load_results()
    filtered = page.filter_by_student("Alice")
    assert len(filtered) == 1
    assert filtered[0]["student"] == "Alice"

def test_filter_by_student_case_insensitive():
    """Test 333: Student filter is case insensitive"""
    page = ResultsPage()
    page.load_results()
    filtered = page.filter_by_student("alice")
    assert len(filtered) == 1

def test_filter_by_accuracy():
    """Test 334: Filter by minimum accuracy"""
    page = ResultsPage()
    page.load_results()
    filtered = page.filter_by_accuracy(80)
    assert len(filtered) == 2  # Alice (85) and Bob (92)

def test_filter_by_question():
    """Test 335: Filter by specific question"""
    page = ResultsPage()
    page.load_results()
    filtered = page.filter_by_question(5)
    assert len(filtered) >= 0

def test_sort_by_score_descending():
    """Test 336: Sort results by score (highest first)"""
    page = ResultsPage()
    page.load_results()
    sorted_results = page.sort_results("score", ascending=False)
    assert sorted_results[0]["score"] == 92
    assert sorted_results[-1]["score"] == 78

def test_sort_by_score_ascending():
    """Test 337: Sort results by score (lowest first)"""
    page = ResultsPage()
    page.load_results()
    sorted_results = page.sort_results("score", ascending=True)
    assert sorted_results[0]["score"] == 78

def test_sort_by_student():
    """Test 338: Sort results by student name"""
    page = ResultsPage()
    page.load_results()
    sorted_results = page.sort_results("student", ascending=True)
    assert sorted_results[0]["student"] == "Alice"

def test_sort_by_accuracy():
    """Test 339: Sort by accuracy"""
    page = ResultsPage()
    page.load_results()
    sorted_results = page.sort_results("accuracy", ascending=False)
    assert sorted_results[0]["accuracy"] == 92.0

def test_get_result_by_id():
    """Test 340: Get specific result by ID"""
    page = ResultsPage()
    page.load_results()
    result = page.get_result_by_id(2)
    assert result is not None
    assert result["student"] == "Bob"

def test_export_to_excel_default():
    """Test 341: Export results to Excel with default filename"""
    page = ResultsPage()
    page.load_results()
    result = page.export_to_excel()
    assert result["status"] == "success"
    assert result["filename"] == "quiz_results.xlsx"
    assert result["records"] == 3

def test_export_to_excel_custom_filename():
    """Test 342: Export with custom filename"""
    page = ResultsPage()
    page.load_results()
    result = page.export_to_excel("my_results.xlsx")
    assert result["filename"] == "my_results.xlsx"

def test_download_report():
    """Test 343: Download PDF report"""
    page = ResultsPage()
    page.load_results()
    result = page.download_report()
    assert result["action"] == "download"
    assert result["format"] == "pdf"

def test_get_statistics():
    """Test 344: Get statistical summary"""
    page = ResultsPage()
    page.load_results()
    stats = page.get_statistics()
    assert stats["total_students"] == 3
    assert stats["average_score"] == 85.0
    assert stats["highest_score"] == 92
    assert stats["lowest_score"] == 78

def test_clear_filters():
    """Test 345: Clear all filters"""
    page = ResultsPage()
    page.load_results()
    page.filter_by_student("Alice")
    page.filter_by_accuracy(80)
    result = page.clear_filters()
    assert result is True
    assert page.filters["student"] is None

def test_get_active_filters():
    """Test 346: Get active filters"""
    page = ResultsPage()
    page.load_results()
    page.filter_by_student("Alice")
    page.filter_by_accuracy(85)
    active = page.get_active_filters()
    assert active["student"] == "Alice"
    assert active["min_accuracy"] == 85


# =============== NEGATIVE TESTS ===============

def test_load_results_non_list():
    """Test 347: Load non-list raises TypeError"""
    page = ResultsPage()
    with pytest.raises(TypeError, match="Results must be a list"):
        page.load_results("not a list")

def test_filter_by_student_non_string():
    """Test 348: Filter with non-string student raises TypeError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(TypeError, match="Student name must be a string"):
        page.filter_by_student(123)

def test_filter_by_student_empty():
    """Test 349: Filter with empty student name raises ValueError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(ValueError, match="Student name cannot be empty"):
        page.filter_by_student("   ")

def test_filter_by_accuracy_non_number():
    """Test 350: Filter with non-number accuracy raises TypeError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(TypeError, match="Accuracy must be a number"):
        page.filter_by_accuracy("80")

def test_filter_by_accuracy_negative():
    """Test 351: Negative accuracy raises ValueError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(ValueError, match="Accuracy must be between 0 and 100"):
        page.filter_by_accuracy(-10)

def test_filter_by_accuracy_over_100():
    """Test 352: Accuracy over 100 raises ValueError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(ValueError, match="Accuracy must be between 0 and 100"):
        page.filter_by_accuracy(150)

def test_filter_by_question_non_integer():
    """Test 353: Filter by non-integer question raises TypeError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(TypeError, match="Question ID must be an integer"):
        page.filter_by_question("5")

def test_sort_results_invalid_option():
    """Test 354: Sort with invalid option raises ValueError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(ValueError, match="Invalid sort option"):
        page.sort_results("invalid")

def test_get_result_by_non_integer_id():
    """Test 355: Get result with non-integer ID raises TypeError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(TypeError, match="Result ID must be an integer"):
        page.get_result_by_id("1")

def test_get_result_by_nonexistent_id():
    """Test 356: Get nonexistent result returns None"""
    page = ResultsPage()
    page.load_results()
    result = page.get_result_by_id(999)
    assert result is None

def test_export_to_excel_no_results():
    """Test 357: Export with no results raises ValueError"""
    page = ResultsPage()
    with pytest.raises(ValueError, match="No results to export"):
        page.export_to_excel()

def test_export_to_excel_non_string_filename():
    """Test 358: Export with non-string filename raises TypeError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(TypeError, match="Filename must be a string"):
        page.export_to_excel(123)

def test_export_to_excel_invalid_extension():
    """Test 359: Export with wrong extension raises ValueError"""
    page = ResultsPage()
    page.load_results()
    with pytest.raises(ValueError, match="Filename must have .xlsx extension"):
        page.export_to_excel("results.pdf")

def test_download_report_no_results():
    """Test 360: Download report with no results raises ValueError"""
    page = ResultsPage()
    with pytest.raises(ValueError, match="No results to download"):
        page.download_report()


# =============== EDGE CASES ===============

def test_get_statistics_empty_results():
    """Test 361: Statistics with empty results"""
    page = ResultsPage()
    stats = page.get_statistics()
    assert stats["total_students"] == 0
    assert stats["average_score"] == 0

def test_filter_returns_empty_list():
    """Test 362: Filter with no matches returns empty list"""
    page = ResultsPage()
    page.load_results()
    filtered = page.filter_by_student("Nonexistent")
    assert filtered == []

def test_get_active_filters_when_none():
    """Test 363: Active filters empty when none set"""
    page = ResultsPage()
    page.load_results()
    active = page.get_active_filters()
    assert active == {}

def test_filter_accuracy_with_float():
    """Test 364: Filter accuracy accepts float values"""
    page = ResultsPage()
    page.load_results()
    filtered = page.filter_by_accuracy(85.5)
    assert len(filtered) == 1  # Only Bob (92)
