using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace CleanMasterPro.Utils.AIService
{
    public class AIServiceExample
    {
        public static async Task RunExample()
        {
            Console.WriteLine("AI Service Example");
            Console.WriteLine("==================");
            
            // 获取AI服务实例
            var aiService = AIServiceFactory.GetAIService();
            
            // 检查AI服务是否可用
            if (aiService.IsAvailable())
            {
                Console.WriteLine("AI Service is available");
                
                // 示例1: 分析文件
                Console.WriteLine("\n1. Analyzing file:");
                string fileAnalysis = await aiService.AnalyzeFile("C:\\example.txt");
                Console.WriteLine(fileAnalysis);
                
                // 示例2: 分类文件
                Console.WriteLine("\n2. Categorizing files:");
                List<string> files = new List<string> { "C:\\example.txt", "C:\\image.jpg", "C:\\video.mp4" };
                List<string> categories = await aiService.CategorizeFiles(files);
                foreach (var category in categories)
                {
                    Console.WriteLine(category);
                }
                
                // 示例3: 生成文件名
                Console.WriteLine("\n3. Generating file name:");
                string newFileName = await aiService.GenerateFileName("C:\\old_file.txt");
                Console.WriteLine($"New file name: {newFileName}");
                
                // 示例4: 获取清理建议
                Console.WriteLine("\n4. Getting cleaning suggestions:");
                string suggestions = await aiService.GetCleaningSuggestions("C:\\");
                Console.WriteLine(suggestions);
            }
            else
            {
                Console.WriteLine("AI Service is not available");
            }
            
            Console.WriteLine("\nExample completed");
        }
    }
}