using System;
using System.Collections.Generic;
using System.Linq;

namespace Quizizz.Core.Pages
{
    /// <summary>
    /// Represents the results view for a completed quiz.  Stores user
    /// performance and allows filtering and sorting.
    /// </summary>
    public class ResultsPage
    {
        public class Result
        {
            public string Username { get; set; } = string.Empty;
            public int Correct { get; set; }
            public int Total { get; set; }
            public TimeSpan TimeTaken { get; set; }

            public double Accuracy => Total > 0 ? (double)Correct / Total : 0;
        }

        private readonly List<Result> _results = new();

        public IReadOnlyCollection<Result> Results => _results.AsReadOnly();

        public void AddResult(string username, int correct, int total, TimeSpan timeTaken)
        {
            if (string.IsNullOrWhiteSpace(username))
            {
                throw new ArgumentException("Username cannot be empty");
            }
            if (correct < 0 || total <= 0 || correct > total)
            {
                throw new ArgumentException("Invalid score values");
            }
            _results.Add(new Result { Username = username, Correct = correct, Total = total, TimeTaken = timeTaken });
        }

        public IEnumerable<Result> GetResultsSortedByAccuracy(bool descending = true)
        {
            return descending
                ? _results.OrderByDescending(r => r.Accuracy).ToList()
                : _results.OrderBy(r => r.Accuracy).ToList();
        }

        public IEnumerable<Result> FilterByUser(string username)
        {
            return _results.Where(r => r.Username.Equals(username, StringComparison.OrdinalIgnoreCase)).ToList();
        }
    }
}