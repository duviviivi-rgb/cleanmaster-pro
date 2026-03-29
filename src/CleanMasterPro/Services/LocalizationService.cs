using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;

namespace CleanMasterPro.Services
{
    public class LocalizationService
    {
        private readonly Dictionary<string, Dictionary<string, string>> translations;
        private string defaultLanguage = "zh-CN";

        public LocalizationService()
        {
            translations = new Dictionary<string, Dictionary<string, string>>();
            LoadTranslations();
        }

        private void LoadTranslations()
        {
            // 加载中文翻译
            translations["zh-CN"] = new Dictionary<string, string>
            {
                { "diskInfo", "磁盘信息" },
                { "cleaningSuggestions", "清理建议" },
                { "systemStatus", "系统状态" },
                { "cpuUsage", "CPU使用率" },
                { "memoryUsage", "内存使用率" },
                { "bootTime", "系统启动时间" },
                { "usedSpace", "已使用" },
                { "tempFiles", "临时文件" },
                { "browserCache", "浏览器缓存" },
                { "systemLogs", "系统日志" },
                { "oldWindowsFiles", "旧版本Windows文件" },
                { "loading", "加载中..." },
                { "version", "CleanMaster Pro v1.0.0" },
                { "help", "帮助" },
                { "about", "关于" }
            };

            // 加载英文翻译
            translations["en-US"] = new Dictionary<string, string>
            {
                { "diskInfo", "Disk Information" },
                { "cleaningSuggestions", "Cleaning Suggestions" },
                { "systemStatus", "System Status" },
                { "cpuUsage", "CPU Usage" },
                { "memoryUsage", "Memory Usage" },
                { "bootTime", "System Boot Time" },
                { "usedSpace", "Used" },
                { "tempFiles", "Temporary Files" },
                { "browserCache", "Browser Cache" },
                { "systemLogs", "System Logs" },
                { "oldWindowsFiles", "Old Windows Files" },
                { "loading", "Loading..." },
                { "version", "CleanMaster Pro v1.0.0" },
                { "help", "Help" },
                { "about", "About" }
            };
        }

        public string GetString(string key, string language = null)
        {
            var lang = language ?? defaultLanguage;
            
            if (translations.ContainsKey(lang) && translations[lang].ContainsKey(key))
            {
                return translations[lang][key];
            }
            
            // 如果找不到翻译，返回键名
            return key;
        }

        public void SetDefaultLanguage(string language)
        {
            if (translations.ContainsKey(language))
            {
                defaultLanguage = language;
            }
        }

        public List<string> GetSupportedLanguages()
        {
            return new List<string>(translations.Keys);
        }
    }
}
