using System;
using System.Linq;
using Quizizz.Core.Pages;
using Xunit;

namespace Quizizz.Tests.Pages
{
    public class ResultsPageTests
    {
        [Fact]
        public void AddResult_Valid_AddsResult()
        {
            var page = new ResultsPage();
            page.AddResult("User1", 8, 10, TimeSpan.FromMinutes(5));
            Assert.Single(page.Results);
            var result = page.Results.First();
            Assert.Equal("User1", result.Username);
            Assert.Equal(0.8, result.Accuracy, 3);
        }

        [Fact]
        public void AddResult_InvalidScore_Throws()
        {
            var page = new ResultsPage();
            Assert.Throws<ArgumentException>(() => page.AddResult("User", -1, 10, TimeSpan.Zero));
            Assert.Throws<ArgumentException>(() => page.AddResult("User", 5, 0, TimeSpan.Zero));
            Assert.Throws<ArgumentException>(() => page.AddResult("User", 5, 4, TimeSpan.Zero));
        }

        [Fact]
        public void FilterByUser_ReturnsOnlyMatching()
        {
            var page = new ResultsPage();
            page.AddResult("A", 5, 10, TimeSpan.Zero);
            page.AddResult("B", 7, 10, TimeSpan.Zero);
            var list = page.FilterByUser("b").ToList();
            Assert.Single(list);
            Assert.Equal("B", list[0].Username);
        }

        [Fact]
        public void GetResultsSortedByAccuracy_Descending()
        {
            var page = new ResultsPage();
            page.AddResult("X", 2, 5, TimeSpan.Zero); // 0.4
            page.AddResult("Y", 4, 5, TimeSpan.Zero); // 0.8
            var sorted = page.GetResultsSortedByAccuracy().ToList();
            Assert.Equal(new[] { "Y", "X" }, sorted.Select(r => r.Username));
        }

        [Fact]
        public void GetResultsSortedByAccuracy_Ascending()
        {
            var page = new ResultsPage();
            page.AddResult("M", 9, 10, TimeSpan.Zero);
            page.AddResult("N", 5, 10, TimeSpan.Zero);
            var sorted = page.GetResultsSortedByAccuracy(descending: false).ToList();
            Assert.Equal(new[] { "N", "M" }, sorted.Select(r => r.Username));
        }
    }
}