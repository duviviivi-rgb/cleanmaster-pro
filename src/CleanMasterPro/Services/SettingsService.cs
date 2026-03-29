using System;
using System.IO;
using System.Text.Json;
using CleanMasterPro.Models;

namespace CleanMasterPro.Services
{
    public class SettingsService
    {
        private readonly string settingsFilePath;

        public SettingsService()
        {
            // 设置文件路径
            var appDataPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            var appFolder = Path.Combine(appDataPath, "CleanMasterPro");
            
            if (!Directory.Exists(appFolder))
            {
                Directory.CreateDirectory(appFolder);
            }
            
            settingsFilePath = Path.Combine(appFolder, "settings.json");
        }

        public UserSettings GetSettings()
        {
            try
            {
                if (File.Exists(settingsFilePath))
                {
                    var json = File.ReadAllText(settingsFilePath);
                    return JsonSerializer.Deserialize<UserSettings>(json);
                }
                else
                {
                    // 返回默认设置
                    return GetDefaultSettings();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"获取设置失败: {ex.Message}");
                return GetDefaultSettings();
            }
        }

        public bool SaveSettings(UserSettings settings)
        {
            try
            {
                var json = JsonSerializer.Serialize(settings, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(settingsFilePath, json);
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"保存设置失败: {ex.Message}");
                return false;
            }
        }

        private UserSettings GetDefaultSettings()
        {
            return new UserSettings
            {
                Language = "zh-CN",
                Theme = "light",
                AutoStart = false,
                DefaultCleanLevel = "standard",
                HistoryRetention = 30
            };
        }
    }
}
