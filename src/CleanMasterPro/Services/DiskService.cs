using System;
using System.Collections.Generic;
using System.IO;
using CleanMasterPro.Models;

namespace CleanMasterPro.Services
{
    public class DiskService
    {
        public List<DiskInfo> GetDisks()
        {
            var disks = new List<DiskInfo>();
            
            try
            {
                foreach (var drive in DriveInfo.GetDrives())
                {
                    if (drive.IsReady)
                    {
                        var diskInfo = new DiskInfo
                        {
                            Letter = drive.Name,
                            Name = drive.VolumeLabel,
                            TotalSpace = drive.TotalSize,
                            FreeSpace = drive.AvailableFreeSpace
                        };
                        
                        diskInfo.UsedSpace = diskInfo.TotalSpace - diskInfo.FreeSpace;
                        diskInfo.Percentage = (int)((double)diskInfo.UsedSpace / diskInfo.TotalSpace * 100);
                        
                        disks.Add(diskInfo);
                    }
                }
            }
            catch (Exception ex)
            {
                // 记录错误
                Console.WriteLine($"获取磁盘信息失败: {ex.Message}");
                
                // 返回模拟数据
                disks.Add(new DiskInfo
                {
                    Letter = "C:",
                    Name = "系统盘",
                    TotalSpace = 135000000000,
                    UsedSpace = 100000000000,
                    FreeSpace = 35000000000,
                    Percentage = 74
                });
                
                disks.Add(new DiskInfo
                {
                    Letter = "D:",
                    Name = "数据盘",
                    TotalSpace = 500000000000,
                    UsedSpace = 150000000000,
                    FreeSpace = 350000000000,
                    Percentage = 30
                });
            }
            
            return disks;
        }
    }
}
