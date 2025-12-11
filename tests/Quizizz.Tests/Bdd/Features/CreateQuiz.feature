Feature: Creating a new quiz
  In order to build content on Quizizz
  As a teacher
  I want to create a new quiz with questions and answers

  Scenario: Create a quiz with a single question and answer
    Given I am on the quiz editor page
    When I add a new question with text "What is the capital of Ukraine?"
    And I add answer option "Kyiv"
    And I set the correct answer to option 1
    Then the quiz should have 1 question
    And the first question should have the correct answer index equal to 0