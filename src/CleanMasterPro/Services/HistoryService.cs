using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using CleanMasterPro.Models;

namespace CleanMasterPro.Services
{
    public class HistoryService
    {
        private readonly string historyFilePath;

        public HistoryService()
        {
            // 历史记录文件路径
            var appDataPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            var appFolder = Path.Combine(appDataPath, "CleanMasterPro");
            
            if (!Directory.Exists(appFolder))
            {
                Directory.CreateDirectory(appFolder);
            }
            
            historyFilePath = Path.Combine(appFolder, "history.json");
        }

        public List<CleanHistory> GetCleanHistory()
        {
            try
            {
                if (File.Exists(historyFilePath))
                {
                    var json = File.ReadAllText(historyFilePath);
                    return JsonSerializer.Deserialize<List<CleanHistory>>(json) ?? new List<CleanHistory>();
                }
                else
                {
                    return new List<CleanHistory>();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"获取清理历史失败: {ex.Message}");
                return new List<CleanHistory>();
            }
        }

        public bool AddCleanHistory(CleanHistory history)
        {
            try
            {
                var histories = GetCleanHistory();
                histories.Add(history);
                
                // 保存历史记录
                var json = JsonSerializer.Serialize(histories, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(historyFilePath, json);
                
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"添加清理历史失败: {ex.Message}");
                return false;
            }
        }

        public bool CleanHistory(int retentionDays)
        {
            try
            {
                var histories = GetCleanHistory();
                var cutoffDate = DateTime.Now.AddDays(-retentionDays);
                
                // 保留指定天数内的历史记录
                var filteredHistories = histories.Where(h => h.Timestamp >= cutoffDate).ToList();
                
                // 保存过滤后的历史记录
                var json = JsonSerializer.Serialize(filteredHistories, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(historyFilePath, json);
                
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"清理历史记录失败: {ex.Message}");
                return false;
            }
        }
    }
}
