using System;
using Quizizz.Core.Pages;
using Xunit;

namespace Quizizz.Tests.Pages
{
    public class HomeworkAssignPageTests
    {
        [Fact]
        public void SetDueDate_FutureDate_SetsProperty()
        {
            var page = new HomeworkAssignPage();
            var future = DateTime.UtcNow.AddDays(1);
            page.SetDueDate(future);
            Assert.Equal(future, page.DueDate);
        }

        [Fact]
        public void SetDueDate_PastDate_Throws()
        {
            var page = new HomeworkAssignPage();
            var past = DateTime.UtcNow.AddDays(-1);
            Assert.Throws<ArgumentException>(() => page.SetDueDate(past));
        }

        [Fact]
        public void AssignToClass_AddsClass()
        {
            var page = new HomeworkAssignPage();
            page.AssignToClass("Class A");
            Assert.Contains("Class A", page.AssignedClasses);
        }

        [Fact]
        public void AssignToClass_Empty_Throws()
        {
            var page = new HomeworkAssignPage();
            Assert.Throws<ArgumentException>(() => page.AssignToClass(" "));
        }

        [Fact]
        public void AssignToClass_Duplicate_NotAddedTwice()
        {
            var page = new HomeworkAssignPage();
            page.AssignToClass("A");
            page.AssignToClass("A");
            Assert.Single(page.AssignedClasses);
        }

        [Fact]
        public void UnassignClass_RemovesClass()
        {
            var page = new HomeworkAssignPage();
            page.AssignToClass("A");
            page.UnassignClass("A");
            Assert.Empty(page.AssignedClasses);
        }
    }
}