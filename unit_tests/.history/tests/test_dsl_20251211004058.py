import pytest
from dsl import StepParser, StepRunner, FeatureParser


# =============== STEP PARSER TESTS ===============

def test_parse_simple_step():
    """Test 128: Parse simple step text"""
    parser = StepParser()
    result = parser.parse("Given user opens quiz")
    assert len(result) == 4

def test_parse_two_words():
    """Test 129: Parse two words"""
    parser = StepParser()
    result = parser.parse("When search")
    assert len(result) == 2

def test_validate_step_given():
    """Test 130: Validate Given step"""
    parser = StepParser()
    assert parser.validate_step("Given user is logged in") is True

def test_validate_step_when():
    """Test 131: Validate When step"""
    parser = StepParser()
    assert parser.validate_step("When user clicks button") is True

def test_validate_step_then():
    """Test 132: Validate Then step"""
    parser = StepParser()
    assert parser.validate_step("Then quiz is displayed") is True

def test_validate_step_and():
    """Test 133: Validate And step"""
    parser = StepParser()
    assert parser.validate_step("And user sees results") is True

def test_validate_step_but():
    """Test 134: Validate But step"""
    parser = StepParser()
    assert parser.validate_step("But error is not shown") is True

def test_validate_step_invalid_keyword():
    """Test 135: Validate invalid keyword"""
    parser = StepParser()
    assert parser.validate_step("Invalid step") is False

def test_extract_keyword_given():
    """Test 136: Extract Given keyword"""
    parser = StepParser()
    result = parser.extract_keyword("Given user opens quiz")
    assert result == "Given"

def test_extract_keyword_when():
    """Test 137: Extract When keyword"""
    parser = StepParser()
    result = parser.extract_keyword("When search executes")
    assert result == "When"

def test_extract_keyword_none():
    """Test 138: Extract keyword from invalid step"""
    parser = StepParser()
    result = parser.extract_keyword("Invalid step")
    assert result is None

def test_parse_parameters_single():
    """Test 139: Parse step with single parameter"""
    parser = StepParser()
    result = parser.parse_parameters("search for 'math'")
    assert "math" in result

def test_parse_parameters_multiple():
    """Test 140: Parse step with multiple parameters"""
    parser = StepParser()
    result = parser.parse_parameters("filter by 'grade' and '5'")
    assert len(result) >= 2

def test_parse_parameters_none():
    """Test 141: Parse step with no parameters"""
    parser = StepParser()
    result = parser.parse_parameters("click button")
    assert len(result) == 0


# =============== STEP RUNNER TESTS ===============

def test_run_single_step():
    """Test 142: Run single step"""
    runner = StepRunner()
    runner.run(["Given user opens quiz"])
    assert len(runner.get_executed_steps()) == 1

def test_run_multiple_steps():
    """Test 143: Run multiple steps"""
    runner = StepRunner()
    runner.run(["Given user opens quiz", "When user clicks start"])
    assert len(runner.get_executed_steps()) == 2

def test_get_executed_steps():
    """Test 144: Get executed steps list"""
    runner = StepRunner()
    runner.run(["Given step"])
    result = runner.get_executed_steps()
    assert "Given step" in result

def test_get_executed_steps_empty():
    """Test 145: Get executed steps when none run"""
    runner = StepRunner()
    result = runner.get_executed_steps()
    assert len(result) == 0

def test_get_failed_steps_empty():
    """Test 146: Get failed steps when none failed"""
    runner = StepRunner()
    runner.run(["Given step"])
    result = runner.get_failed_steps()
    assert len(result) == 0

def test_mark_failed():
    """Test 147: Mark step as failed"""
    runner = StepRunner()
    runner.run(["Given step"])
    runner.mark_failed("Given step")
    failed = runner.get_failed_steps()
    assert "Given step" in failed

def test_reset_runner():
    """Test 148: Reset runner clears executed steps"""
    runner = StepRunner()
    runner.run(["Given step"])
    runner.reset()
    assert len(runner.get_executed_steps()) == 0

def test_reset_clears_failed():
    """Test 149: Reset clears failed steps"""
    runner = StepRunner()
    runner.run(["Given step"])
    runner.mark_failed("Given step")
    runner.reset()
    assert len(runner.get_failed_steps()) == 0

def test_get_execution_count():
    """Test 150: Get execution count"""
    runner = StepRunner()
    runner.run(["Given step"])
    assert runner.get_execution_count() == 1

def test_execution_count_accumulates():
    """Test 151: Execution count accumulates"""
    runner = StepRunner()
    runner.run(["Given step1"])
    runner.run(["When step2"])
    assert runner.get_execution_count() == 2

def test_get_executed_steps_returns_copy():
    """Test 152: get_executed_steps returns copy"""
    runner = StepRunner()
    runner.run(["Given step"])
    steps = runner.get_executed_steps()
    steps.append("fake step")
    assert "fake step" not in runner.get_executed_steps()


# =============== FEATURE PARSER TESTS ===============

def test_parse_feature_single_line():
    """Test 153: Parse single line feature"""
    parser = FeatureParser()
    result = parser.parse_feature("Feature: Quiz search")
    assert "Quiz search" in result

def test_parse_feature_multiple_lines():
    """Test 154: Parse multi-line feature"""
    parser = FeatureParser()
    result = parser.parse_feature("Feature: Search\nAs a user\nI want to search")
    assert "Search" in result

def test_parse_feature_strips_whitespace():
    """Test 155: Parse feature strips whitespace"""
    parser = FeatureParser()
    result = parser.parse_feature("  Feature: Search  ")
    assert result.strip() == "Feature: Search"

def test_get_feature_count():
    """Test 156: Get feature count"""
    parser = FeatureParser()
    parser.parse_feature("Feature: Search")
    parser.parse_feature("Feature: Filter")
    assert parser.get_feature_count() == 2

def test_feature_count_initial():
    """Test 157: Initial feature count is 0"""
    parser = FeatureParser()
    assert parser.get_feature_count() == 0


# =============== NEGATIVE TESTS ===============

def test_parse_empty_string():
    """Test 158: Parse empty string raises error"""
    parser = StepParser()
    with pytest.raises(ValueError, match="Step cannot be empty"):
        parser.parse("")

def test_parse_whitespace_only():
    """Test 159: Parse whitespace only raises error"""
    parser = StepParser()
    with pytest.raises(ValueError, match="Step cannot be empty"):
        parser.parse("   ")

def test_parse_non_string():
    """Test 160: Parse non-string raises error"""
    parser = StepParser()
    with pytest.raises(TypeError, match="Step must be a string"):
        parser.parse(123)

def test_validate_empty_step():
    """Test 161: Validate empty step returns False"""
    parser = StepParser()
    assert parser.validate_step("") is False

def test_run_non_list():
    """Test 162: Run with non-list raises error"""
    runner = StepRunner()
    with pytest.raises(TypeError, match="Steps must be a list"):
        runner.run("not a list")

def test_mark_failed_not_executed():
    """Test 163: Mark non-executed step as failed raises error"""
    runner = StepRunner()
    with pytest.raises(ValueError, match="Step was not executed"):
        runner.mark_failed("nonexistent step")

def test_parse_feature_non_string():
    """Test 164: Parse non-string feature raises error"""
    parser = FeatureParser()
    with pytest.raises(TypeError, match="Feature must be a string"):
        parser.parse_feature(123)

def test_parse_feature_empty():
    """Test 165: Parse empty feature raises error"""
    parser = FeatureParser()
    with pytest.raises(ValueError, match="Feature cannot be empty"):
        parser.parse_feature("")

def test_parse_feature_whitespace():
    """Test 166: Parse whitespace feature raises error"""
    parser = FeatureParser()
    with pytest.raises(ValueError, match="Feature cannot be empty"):
        parser.parse_feature("   ")
