using System;

namespace CleanMasterPro.Models
{
    public class UserSettings
    {
        public string Language { get; set; }
        public string Theme { get; set; }
        public bool AutoStart { get; set; }
        public string DefaultCleanLevel { get; set; }
        public int HistoryRetention { get; set; }
    }

    public class AutoCleanSettings
    {
        public bool Enabled { get; set; }
        public string Frequency { get; set; }
        public string Time { get; set; }
        public string Disk { get; set; }
        public string[] FileTypes { get; set; }
    }

    public class CleanHistory
    {
        public string Id { get; set; }
        public DateTime Timestamp { get; set; }
        public string Disk { get; set; }
        public string CleanType { get; set; }
        public long SpaceSaved { get; set; }
        public int FilesDeleted { get; set; }
    }
}
