using System;
using System.Linq;
using Quizizz.Core.Pages;
using Xunit;

namespace Quizizz.Tests.Pages
{
    public class LiveSessionPageTests
    {
        [Fact]
        public void GenerateSessionCode_ReturnsSixDigits()
        {
            var page = new LiveSessionPage();
            var code = page.GenerateSessionCode();
            Assert.Equal(6, code.Length);
            Assert.True(int.TryParse(code, out _));
        }

        [Fact]
        public void AddParticipant_AddsName()
        {
            var page = new LiveSessionPage();
            page.AddParticipant("Alice");
            Assert.Contains("Alice", page.Participants);
        }

        [Fact]
        public void AddParticipant_Empty_Throws()
        {
            var page = new LiveSessionPage();
            Assert.Throws<ArgumentException>(() => page.AddParticipant(""));
        }

        [Fact]
        public void RemoveParticipant_RemovesName()
        {
            var page = new LiveSessionPage();
            page.AddParticipant("Bob");
            page.RemoveParticipant("Bob");
            Assert.DoesNotContain("Bob", page.Participants);
        }

        [Fact]
        public void StartSession_WithoutCode_Throws()
        {
            var page = new LiveSessionPage();
            page.AddParticipant("A");
            var ex = Assert.Throws<InvalidOperationException>(() => page.StartSession());
            Assert.Equal("Generate a session code before starting", ex.Message);
        }

        [Fact]
        public void StartSession_WithoutParticipants_Throws()
        {
            var page = new LiveSessionPage();
            page.GenerateSessionCode();
            var ex = Assert.Throws<InvalidOperationException>(() => page.StartSession());
            Assert.Equal("Cannot start session without participants", ex.Message);
        }

        [Fact]
        public void StartSession_WithCodeAndParticipants_SetsStarted()
        {
            var page = new LiveSessionPage();
            page.GenerateSessionCode();
            page.AddParticipant("Alice");
            page.StartSession();
            Assert.True(page.Started);
        }
    }
}