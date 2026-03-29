using System;
using System.Collections.Generic;

namespace CleanMasterPro.Models
{
    public class FileTypeInfo
    {
        public string Type { get; set; }
        public long Size { get; set; }
        public int Percentage { get; set; }
    }

    public class ScanFileInfo
    {
        public string Path { get; set; }
        public long Size { get; set; }
        public DateTime LastModified { get; set; }
        public string Type { get; set; }
    }

    public class QuickScanResult
    {
        public long TotalSpace { get; set; }
        public long UsedSpace { get; set; }
        public long CleanableSpace { get; set; }
        public List<FileTypeInfo> FileTypes { get; set; }
    }

    public class DeepScanResult
    {
        public long TotalSpace { get; set; }
        public long UsedSpace { get; set; }
        public long CleanableSpace { get; set; }
        public List<FileTypeInfo> FileTypes { get; set; }
        public List<ScanFileInfo> Files { get; set; }
    }

    public class IntelligentAnalysisResult
    {
        public List<UsageFrequencyInfo> UsageFrequency { get; set; }
        public List<string> Suggestions { get; set; }
        public long EstimatedSpaceSaved { get; set; }
    }

    public class UsageFrequencyInfo
    {
        public string Range { get; set; }
        public int Percentage { get; set; }
    }
}
