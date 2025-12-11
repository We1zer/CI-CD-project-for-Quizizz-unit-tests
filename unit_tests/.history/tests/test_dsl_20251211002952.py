import pytest
from dsl import StepParser, ScenarioRunner, FeatureParser


# ============== STEP PARSER TESTS ==============

def test_parse_simple_step():
    """Test 119: Parse simple step text"""
    parser = StepParser()
    result = parser.parse("Given user is logged in")
    assert len(result) == 5
    assert result[0] == "Given"


def test_parse_two_words():
    """Test 120: Parse step with two words"""
    parser = StepParser()
    result = parser.parse("hello world")
    assert result == ["hello", "world"]


def test_validate_step_given():
    """Test 121: Validate step with Given keyword"""
    parser = StepParser()
    assert parser.validate_step("Given user exists") is True


def test_validate_step_when():
    """Test 122: Validate step with When keyword"""
    parser = StepParser()
    assert parser.validate_step("When button clicked") is True


def test_validate_step_then():
    """Test 123: Validate step with Then keyword"""
    parser = StepParser()
    assert parser.validate_step("Then page loads") is True


def test_validate_step_and():
    """Test 124: Validate step with And keyword"""
    parser = StepParser()
    assert parser.validate_step("And form is visible") is True


def test_validate_step_but():
    """Test 125: Validate step with But keyword"""
    parser = StepParser()
    assert parser.validate_step("But error is shown") is True


def test_validate_step_invalid_keyword():
    """Test 126: Validate step without keyword returns False"""
    parser = StepParser()
    assert parser.validate_step("Invalid step format") is False


def test_extract_keyword_given():
    """Test 127: Extract Given keyword from step"""
    parser = StepParser()
    keyword = parser.extract_keyword("Given precondition met")
    assert keyword == "Given"


def test_extract_keyword_when():
    """Test 128: Extract When keyword from step"""
    parser = StepParser()
    keyword = parser.extract_keyword("When action performed")
    assert keyword == "When"


def test_extract_keyword_none():
    """Test 129: Extract keyword returns None for invalid step"""
    parser = StepParser()
    keyword = parser.extract_keyword("no keyword here")
    assert keyword is None


def test_parse_parameters_single():
    """Test 130: Parse single parameter from step"""
    parser = StepParser()
    params = parser.parse_parameters('Given user "John" exists')
    assert len(params) == 1
    assert params[0] == "John"


def test_parse_parameters_multiple():
    """Test 131: Parse multiple parameters from step"""
    parser = StepParser()
    params = parser.parse_parameters('When user "John" enters "password123"')
    assert len(params) == 2
    assert params[0] == "John"
    assert params[1] == "password123"


def test_parse_parameters_none():
    """Test 132: Parse step with no parameters"""
    parser = StepParser()
    params = parser.parse_parameters("Given user is logged in")
    assert len(params) == 0


# ============== SCENARIO RUNNER TESTS ==============

def test_run_single_step():
    """Test 133: Run single step"""
    runner = ScenarioRunner()
    result = runner.run(["step1"])
    assert result == ["RUN:step1"]


def test_run_multiple_steps():
    """Test 134: Run multiple steps"""
    runner = ScenarioRunner()
    result = runner.run(["step1", "step2", "step3"])
    assert len(result) == 3
    assert result[0] == "RUN:step1"


def test_get_executed_steps():
    """Test 135: Get list of executed steps"""
    runner = ScenarioRunner()
    runner.run(["A", "B"])
    executed = runner.get_executed_steps()
    assert executed == ["A", "B"]


def test_get_executed_steps_empty():
    """Test 136: Get executed steps before running any"""
    runner = ScenarioRunner()
    assert len(runner.get_executed_steps()) == 0


def test_get_failed_steps_empty():
    """Test 137: Get failed steps when none failed"""
    runner = ScenarioRunner()
    runner.run(["A"])
    assert len(runner.get_failed_steps()) == 0


def test_mark_failed():
    """Test 138: Mark step as failed"""
    runner = ScenarioRunner()
    runner.run(["A", "B"])
    runner.mark_failed("A")
    assert "A" in runner.get_failed_steps()


def test_reset_runner():
    """Test 139: Reset runner clears executed steps"""
    runner = ScenarioRunner()
    runner.run(["A", "B"])
    runner.reset()
    assert len(runner.get_executed_steps()) == 0


def test_reset_clears_failed():
    """Test 140: Reset runner clears failed steps"""
    runner = ScenarioRunner()
    runner.run(["A"])
    runner.mark_failed("A")
    runner.reset()
    assert len(runner.get_failed_steps()) == 0


def test_get_execution_count():
    """Test 141: Get correct execution count"""
    runner = ScenarioRunner()
    runner.run(["A", "B", "C"])
    assert runner.get_execution_count() == 3


def test_execution_count_accumulates():
    """Test 142: Execution count accumulates across runs"""
    runner = ScenarioRunner()
    runner.run(["A"])
    runner.run(["B", "C"])
    assert runner.get_execution_count() == 3


def test_get_executed_steps_returns_copy():
    """Test 143: get_executed_steps returns independent copy"""
    runner = ScenarioRunner()
    runner.run(["A"])
    steps = runner.get_executed_steps()
    steps.append("B")
    assert "B" not in runner.get_executed_steps()


# ============== FEATURE PARSER TESTS ==============

def test_parse_feature_single_line():
    """Test 144: Parse feature with single line"""
    parser = FeatureParser()
    result = parser.parse_feature("Feature: Login")
    assert len(result) == 1
    assert result[0] == "Feature: Login"


def test_parse_feature_multiple_lines():
    """Test 145: Parse feature with multiple lines"""
    parser = FeatureParser()
    text = "Feature: Login\nScenario: Success\nGiven user exists"
    result = parser.parse_feature(text)
    assert len(result) == 3


def test_parse_feature_strips_whitespace():
    """Test 146: Parse feature strips extra whitespace"""
    parser = FeatureParser()
    text = "  Feature: Login  \n  Scenario: Test  "
    result = parser.parse_feature(text)
    assert result[0] == "Feature: Login"
    assert result[1] == "Scenario: Test"


def test_get_feature_count():
    """Test 147: Get correct feature count"""
    parser = FeatureParser()
    parser.parse_feature("Feature: One")
    parser.parse_feature("Feature: Two")
    assert parser.get_feature_count() == 2


def test_feature_count_initial():
    """Test 148: Initial feature count is zero"""
    parser = FeatureParser()
    assert parser.get_feature_count() == 0


# ============== NEGATIVE TESTS ==============

def test_parse_empty_string():
    """Test 149: Parse empty string raises ValueError"""
    parser = StepParser()
    with pytest.raises(ValueError, match="Invalid step"):
        parser.parse("")


def test_parse_whitespace_only():
    """Test 150: Parse whitespace only raises ValueError"""
    parser = StepParser()
    with pytest.raises(ValueError, match="Invalid step"):
        parser.parse("   ")


def test_parse_non_string():
    """Test 151: Parse non-string raises ValueError"""
    parser = StepParser()
    with pytest.raises(ValueError):
        parser.parse(123)


def test_validate_empty_step():
    """Test 152: Validate empty step raises ValueError"""
    parser = StepParser()
    with pytest.raises(ValueError, match="Step cannot be empty"):
        parser.validate_step("")


def test_run_non_list():
    """Test 153: Run with non-list raises TypeError"""
    runner = ScenarioRunner()
    with pytest.raises(TypeError, match="Steps must be list"):
        runner.run("not a list")


def test_mark_failed_not_executed():
    """Test 154: Mark non-executed step as failed raises ValueError"""
    runner = ScenarioRunner()
    with pytest.raises(ValueError, match="Step was not executed"):
        runner.mark_failed("A")


def test_parse_feature_non_string():
    """Test 155: Parse feature with non-string raises TypeError"""
    parser = FeatureParser()
    with pytest.raises(TypeError, match="Feature text must be string"):
        parser.parse_feature(123)


def test_parse_feature_empty():
    """Test 156: Parse empty feature text raises ValueError"""
    parser = FeatureParser()
    with pytest.raises(ValueError, match="Feature text cannot be empty"):
        parser.parse_feature("")


def test_parse_feature_whitespace():
    """Test 157: Parse whitespace feature text raises ValueError"""
    parser = FeatureParser()
    with pytest.raises(ValueError, match="Feature text cannot be empty"):
        parser.parse_feature("   \n   ")
