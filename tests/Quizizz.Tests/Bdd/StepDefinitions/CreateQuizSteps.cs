using System;
using Quizizz.Core.Pages;
using TechTalk.SpecFlow;
using Xunit;

namespace Quizizz.Tests.Bdd.StepDefinitions
{
    [Binding]
    public class CreateQuizSteps
    {
        private readonly QuizEditorPage _editor = new();
        private QuizEditorPage.Question? _currentQuestion;

        [Given("I am on the quiz editor page")]
        public void GivenIAmOnTheQuizEditorPage()
        {
            // Nothing to do here in the stub implementation
        }

        [When("I add a new question with text \"([^\"]*)\"")] 
        public void WhenIAddANewQuestionWithText(string text)
        {
            _currentQuestion = _editor.AddQuestion(text);
        }

        [When("I add answer option \"([^\"]*)\"")]
        public void WhenIAddAnswerOption(string option)
        {
            if (_currentQuestion == null) throw new InvalidOperationException("No question to add answer to");
            _editor.AddAnswer(_currentQuestion, option);
        }

        [When("I set the correct answer to option (\\d+)")]
        public void WhenISetTheCorrectAnswerToOption(int optionNumber)
        {
            if (_currentQuestion == null) throw new InvalidOperationException("No question to set correct answer");
            // optionNumber is 1-based in the feature, convert to 0-based index
            _editor.SetCorrectAnswer(_currentQuestion, optionNumber - 1);
        }

        [Then("the quiz should have (\\d+) question")]
        public void ThenTheQuizShouldHaveQuestion(int expectedCount)
        {
            Assert.Equal(expectedCount, _editor.Questions.Count);
        }

        [Then("the first question should have the correct answer index equal to (\\d+)")]
        public void ThenTheFirstQuestionShouldHaveTheCorrectAnswerIndexEqualTo(int expectedIndex)
        {
            Assert.Equal(expectedIndex, _editor.Questions[0].CorrectIndex);
        }
    }
}