using System;
using System.Collections.Generic;
using System.IO;
using CleanMasterPro.Models;

namespace CleanMasterPro.Services
{
    public class ScanService
    {
        public QuickScanResult QuickScan(string disk = "C:")
        {
            try
            {
                var result = new QuickScanResult
                {
                    TotalSpace = 135000000000,
                    UsedSpace = 100000000000,
                    CleanableSpace = 2500000000,
                    FileTypes = new List<FileTypeInfo>
                    {
                        new FileTypeInfo { Type = "临时文件", Size = 1000000000, Percentage = 40 },
                        new FileTypeInfo { Type = "浏览器缓存", Size = 800000000, Percentage = 32 },
                        new FileTypeInfo { Type = "系统日志", Size = 400000000, Percentage = 16 },
                        new FileTypeInfo { Type = "应用程序缓存", Size = 300000000, Percentage = 12 }
                    }
                };
                
                return result;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"快速扫描失败: {ex.Message}");
                throw;
            }
        }

        public DeepScanResult DeepScan(string disk = "C:")
        {
            try
            {
                var result = new DeepScanResult
                {
                    TotalSpace = 135000000000,
                    UsedSpace = 100000000000,
                    CleanableSpace = 5000000000,
                    FileTypes = new List<FileTypeInfo>
                    {
                        new FileTypeInfo { Type = "临时文件", Size = 1500000000, Percentage = 30 },
                        new FileTypeInfo { Type = "浏览器缓存", Size = 1200000000, Percentage = 24 },
                        new FileTypeInfo { Type = "系统日志", Size = 800000000, Percentage = 16 },
                        new FileTypeInfo { Type = "应用程序缓存", Size = 700000000, Percentage = 14 },
                        new FileTypeInfo { Type = "系统更新文件", Size = 500000000, Percentage = 10 },
                        new FileTypeInfo { Type = "旧版本Windows文件", Size = 300000000, Percentage = 6 }
                    },
                    Files = new List<ScanFileInfo>
                    {
                        new ScanFileInfo { Path = "C:\\Temp\\temp1.txt", Size = 100000000, LastModified = DateTime.Now.AddDays(-1), Type = "临时文件" },
                        new ScanFileInfo { Path = "C:\\Temp\\temp2.txt", Size = 200000000, LastModified = DateTime.Now.AddDays(-2), Type = "临时文件" },
                        new ScanFileInfo { Path = "C:\\Users\\User\\AppData\\Local\\Temp\\cache1.dat", Size = 500000000, LastModified = DateTime.Now.AddDays(-3), Type = "浏览器缓存" },
                        new ScanFileInfo { Path = "C:\\Windows\\Logs\\System\\system1.log", Size = 300000000, LastModified = DateTime.Now.AddDays(-7), Type = "系统日志" }
                    }
                };
                
                return result;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"深度扫描失败: {ex.Message}");
                throw;
            }
        }

        public IntelligentAnalysisResult IntelligentAnalysis(string disk = "C:")
        {
            try
            {
                var result = new IntelligentAnalysisResult
                {
                    UsageFrequency = new List<UsageFrequencyInfo>
                    {
                        new UsageFrequencyInfo { Range = "最近30天使用的文件", Percentage = 65 },
                        new UsageFrequencyInfo { Range = "30-90天未使用的文件", Percentage = 20 },
                        new UsageFrequencyInfo { Range = "90天以上未使用的文件", Percentage = 15 }
                    },
                    Suggestions = new List<string>
                    {
                        "清理90天以上未使用的文件，可释放约1.2 GB空间",
                        "清理临时文件和浏览器缓存，可释放约800 MB空间",
                        "清理系统日志文件，可释放约500 MB空间"
                    },
                    EstimatedSpaceSaved = 2500000000
                };
                
                return result;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"智能分析失败: {ex.Message}");
                throw;
            }
        }
    }
}
