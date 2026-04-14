using System;

namespace CleanMasterPro.Models
{
    public class DiskInfo
    {
        public string Letter { get; set; }
        public string Name { get; set; }
        public long TotalSpace { get; set; }
        public long UsedSpace { get; set; }
        public long FreeSpace { get; set; }
        public int Percentage { get; set; }
    }
}
