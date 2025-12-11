using System;
using System.Linq;
using Quizizz.Core.Pages;
using Xunit;

namespace Quizizz.Tests.Pages
{
    public class DashboardPageTests
    {
        [Fact]
        public void AddQuiz_AddsQuizToList()
        {
            var page = new DashboardPage();
            page.AddQuiz("Math Quiz");
            Assert.Contains("Math Quiz", page.Quizzes);
        }

        [Fact]
        public void AddQuiz_EmptyName_Throws()
        {
            var page = new DashboardPage();
            Assert.Throws<ArgumentException>(() => page.AddQuiz(""));
        }

        [Fact]
        public void RemoveQuiz_RemovesExistingQuiz()
        {
            var page = new DashboardPage(new[] { "Quiz A", "Quiz B" });
            page.RemoveQuiz("Quiz B");
            Assert.DoesNotContain("Quiz B", page.Quizzes);
        }

        [Fact]
        public void RemoveQuiz_NonExisting_Throws()
        {
            var page = new DashboardPage(new[] { "Quiz A" });
            Assert.Throws<InvalidOperationException>(() => page.RemoveQuiz("Quiz X"));
        }

        [Fact]
        public void SearchQuiz_ReturnsMatches()
        {
            var page = new DashboardPage(new[] { "Math", "Science", "Mathematics" });
            var results = page.SearchQuiz("math").ToList();
            Assert.Equal(2, results.Count);
            Assert.Contains("Math", results);
            Assert.Contains("Mathematics", results);
        }

        [Fact]
        public void SearchQuiz_Null_ReturnsAll()
        {
            var page = new DashboardPage(new[] { "Quiz1", "Quiz2" });
            var results = page.SearchQuiz(null).ToList();
            Assert.Equal(2, results.Count);
        }
    }
}