using System;
using System.Collections.Generic;

namespace Quizizz.Core.Pages
{
    /// <summary>
    /// Represents the quiz editor page where the author can build or edit
    /// quizzes by adding questions, answers and configuring settings.
    /// </summary>
    public class QuizEditorPage
    {
        public class Question
        {
            public string Text { get; set; } = string.Empty;
            public List<string> Options { get; } = new();
            public int CorrectIndex { get; set; } = -1;
        }

        private readonly List<Question> _questions = new();
        public IReadOnlyList<Question> Questions => _questions.AsReadOnly();

        public Question AddQuestion(string text)
        {
            if (string.IsNullOrWhiteSpace(text))
            {
                throw new ArgumentException("Question text cannot be empty");
            }
            var q = new Question { Text = text };
            _questions.Add(q);
            return q;
        }

        public void RemoveQuestion(int index)
        {
            if (index < 0 || index >= _questions.Count)
            {
                throw new ArgumentOutOfRangeException(nameof(index), "Invalid question index");
            }
            _questions.RemoveAt(index);
        }

        public void AddAnswer(Question question, string answer)
        {
            if (!_questions.Contains(question))
            {
                throw new InvalidOperationException("Question does not belong to this quiz");
            }
            if (string.IsNullOrWhiteSpace(answer))
            {
                throw new ArgumentException("Answer text cannot be empty");
            }
            question.Options.Add(answer);
        }

        public void SetCorrectAnswer(Question question, int optionIndex)
        {
            if (!_questions.Contains(question))
            {
                throw new InvalidOperationException("Question does not belong to this quiz");
            }
            if (optionIndex < 0 || optionIndex >= question.Options.Count)
            {
                throw new ArgumentOutOfRangeException(nameof(optionIndex), "Invalid option index");
            }
            question.CorrectIndex = optionIndex;
        }

        public void EditQuestionText(Question question, string newText)
        {
            if (!_questions.Contains(question))
            {
                throw new InvalidOperationException("Question does not belong to this quiz");
            }
            if (string.IsNullOrWhiteSpace(newText))
            {
                throw new ArgumentException("Question text cannot be empty");
            }
            question.Text = newText;
        }
    }
}