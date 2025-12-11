using System;
using System.Collections.Generic;

namespace Quizizz.Core.Pages
{
    /// <summary>
    /// Represents the page used to configure and assign a quiz as a homework
    /// activity.  Supports setting the due date and target classes.
    /// </summary>
    public class HomeworkAssignPage
    {
        public DateTime? DueDate { get; private set; }
        private readonly List<string> _assignedClasses = new();
        public IReadOnlyCollection<string> AssignedClasses => _assignedClasses.AsReadOnly();

        public void SetDueDate(DateTime date)
        {
            if (date <= DateTime.UtcNow)
            {
                throw new ArgumentException("Due date must be in the future");
            }
            DueDate = date;
        }

        public void AssignToClass(string className)
        {
            if (string.IsNullOrWhiteSpace(className))
            {
                throw new ArgumentException("Class name cannot be empty");
            }
            if (_assignedClasses.Contains(className)) return;
            _assignedClasses.Add(className);
        }

        public void UnassignClass(string className)
        {
            _assignedClasses.Remove(className);
        }
    }
}