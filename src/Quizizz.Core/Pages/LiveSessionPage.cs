using System;
using System.Collections.Generic;
using System.Linq;

namespace Quizizz.Core.Pages
{
    /// <summary>
    /// Represents a live quiz session.  Handles code generation and
    /// participant management.
    /// </summary>
    public class LiveSessionPage
    {
        private readonly HashSet<string> _participants = new();
        private bool _started;
        private string _sessionCode = string.Empty;

        public IEnumerable<string> Participants => _participants;
        public bool Started => _started;
        public string SessionCode => _sessionCode;

        public string GenerateSessionCode()
        {
            // Generate a simple 6‑digit code for demonstration.  In a real
            // application this would come from the server.
            var rng = new Random();
            _sessionCode = rng.Next(100000, 999999).ToString();
            return _sessionCode;
        }

        public void AddParticipant(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
            {
                throw new ArgumentException("Participant name cannot be empty");
            }
            _participants.Add(name);
        }

        public void RemoveParticipant(string name)
        {
            _participants.Remove(name);
        }

        public void StartSession()
        {
            if (string.IsNullOrEmpty(_sessionCode))
            {
                throw new InvalidOperationException("Generate a session code before starting");
            }
            if (_participants.Count == 0)
            {
                throw new InvalidOperationException("Cannot start session without participants");
            }
            _started = true;
        }
    }
}