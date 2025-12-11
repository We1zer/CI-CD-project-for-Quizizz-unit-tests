using System;
using System.Collections.Generic;
using System.Linq;

namespace Quizizz.Core.Pages
{
    /// <summary>
    /// Represents the dashboard page where the user can browse existing
    /// quizzes and create new ones.
    /// </summary>
    public class DashboardPage
    {
        private readonly List<string> _quizzes = new();

        public IEnumerable<string> Quizzes => _quizzes.AsReadOnly();

        public DashboardPage(IEnumerable<string>? initialQuizzes = null)
        {
            if (initialQuizzes != null)
            {
                _quizzes.AddRange(initialQuizzes);
            }
        }

        public void AddQuiz(string quizName)
        {
            if (string.IsNullOrWhiteSpace(quizName))
            {
                throw new ArgumentException("Quiz name cannot be empty");
            }
            _quizzes.Add(quizName);
        }

        public void RemoveQuiz(string quizName)
        {
            if (!_quizzes.Remove(quizName))
            {
                throw new InvalidOperationException($"Quiz '{quizName}' not found");
            }
        }

        public IEnumerable<string> SearchQuiz(string searchTerm)
        {
            if (searchTerm == null) searchTerm = string.Empty;
            return _quizzes.Where(q => q.Contains(searchTerm, StringComparison.OrdinalIgnoreCase)).ToList();
        }
    }
}