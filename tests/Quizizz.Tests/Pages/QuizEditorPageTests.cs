using System;
using Quizizz.Core.Pages;
using Xunit;

namespace Quizizz.Tests.Pages
{
    public class QuizEditorPageTests
    {
        [Fact]
        public void AddQuestion_ValidText_AddsQuestion()
        {
            var editor = new QuizEditorPage();
            var question = editor.AddQuestion("What is 2+2?");
            Assert.Single(editor.Questions);
            Assert.Equal("What is 2+2?", question.Text);
        }

        [Fact]
        public void AddQuestion_EmptyText_Throws()
        {
            var editor = new QuizEditorPage();
            Assert.Throws<ArgumentException>(() => editor.AddQuestion(""));
        }

        [Fact]
        public void RemoveQuestion_RemovesByIndex()
        {
            var editor = new QuizEditorPage();
            editor.AddQuestion("Q1");
            editor.AddQuestion("Q2");
            editor.RemoveQuestion(0);
            Assert.Single(editor.Questions);
            Assert.Equal("Q2", editor.Questions[0].Text);
        }

        [Fact]
        public void RemoveQuestion_InvalidIndex_Throws()
        {
            var editor = new QuizEditorPage();
            Assert.Throws<ArgumentOutOfRangeException>(() => editor.RemoveQuestion(0));
        }

        [Fact]
        public void AddAnswer_AddsAnswerToQuestion()
        {
            var editor = new QuizEditorPage();
            var question = editor.AddQuestion("Capital of France?");
            editor.AddAnswer(question, "Paris");
            Assert.Single(question.Options);
            Assert.Equal("Paris", question.Options[0]);
        }

        [Fact]
        public void AddAnswer_EmptyText_Throws()
        {
            var editor = new QuizEditorPage();
            var question = editor.AddQuestion("Test?");
            Assert.Throws<ArgumentException>(() => editor.AddAnswer(question, ""));
        }

        [Fact]
        public void SetCorrectAnswer_SetsIndex()
        {
            var editor = new QuizEditorPage();
            var question = editor.AddQuestion("1+1?");
            editor.AddAnswer(question, "1");
            editor.AddAnswer(question, "2");
            editor.SetCorrectAnswer(question, 1);
            Assert.Equal(1, question.CorrectIndex);
        }

        [Fact]
        public void SetCorrectAnswer_InvalidIndex_Throws()
        {
            var editor = new QuizEditorPage();
            var question = editor.AddQuestion("2+2?");
            editor.AddAnswer(question, "4");
            Assert.Throws<ArgumentOutOfRangeException>(() => editor.SetCorrectAnswer(question, 2));
        }
    }
}