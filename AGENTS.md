# AI开发指令

## 1. 项目概述

本项目是一个智能磁盘清理与数据治理工具，集成了AI功能以提供更智能的文件分析、分类和清理建议。本文档提供了AI服务的开发指令和使用指南。

## 2. AI服务架构

### 2.1 核心组件

- **IAIService接口**：定义AI服务的核心功能
- **MLNetAIService**：基于ML.NET的本地AI服务实现
- **AIServiceFactory**：AI服务的工厂类，负责创建和管理AI服务实例

### 2.2 目录结构

```
src/CleanMasterPro/Utils/AIService/
├── IAIService.cs         # AI服务接口
├── MLNetAIService.cs     # ML.NET实现
├── AIServiceFactory.cs   # 服务工厂
└── AIServiceExample.cs   # 使用示例
```

## 3. 开发环境设置

### 3.1 依赖项

- **Microsoft.ML**：ML.NET机器学习库
- **.NET Framework 4.7.2**：项目运行环境

### 3.2 安装依赖

使用NuGet包管理器安装以下包：

```
Install-Package Microsoft.ML -Version 1.5.5
```

## 4. AI服务使用指南

### 4.1 获取AI服务实例

```csharp
using CleanMasterPro.Utils.AIService;

// 获取AI服务实例
var aiService = AIServiceFactory.GetAIService();

// 检查服务是否可用
if (aiService.IsAvailable())
{
    // 服务可用，执行AI操作
}
```

### 4.2 文件分析

```csharp
// 分析文件
string analysis = await aiService.AnalyzeFile("C:\\example.txt");
Console.WriteLine(analysis);
// 输出示例: 文件类型: .txt, 大小: 1024 bytes, 最后修改时间: 2026-03-29 10:00:00
```

### 4.3 文件分类

```csharp
// 分类文件列表
List<string> files = new List<string> { "C:\\example.txt", "C:\\image.jpg", "C:\\video.mp4" };
List<string> categories = await aiService.CategorizeFiles(files);
foreach (var category in categories)
{
    Console.WriteLine(category);
}
// 输出示例:
// C:\example.txt -> 文档
// C:\image.jpg -> 图片
// C:\video.mp4 -> 视频
```

### 4.4 文件名生成

```csharp
// 生成优化的文件名
string newFileName = await aiService.GenerateFileName("C:\\old_file.txt");
Console.WriteLine($"New file name: {newFileName}");
// 输出示例: New file name: old_file_optimized.txt
```

### 4.5 清理建议

```csharp
// 获取磁盘清理建议
string suggestions = await aiService.GetCleaningSuggestions("C:\\");
Console.WriteLine(suggestions);
// 输出示例: 建议清理临时文件、浏览器缓存和系统日志文件。
```

## 5. 扩展AI服务

### 5.1 实现自定义AI服务

如果需要使用其他AI服务（如Azure OpenAI或OpenAI API），可以通过实现IAIService接口来扩展：

```csharp
public class CustomAIService : IAIService
{
    public async Task<string> AnalyzeFile(string filePath)
    {
        // 实现自定义文件分析逻辑
    }
    
    public async Task<List<string>> CategorizeFiles(List<string> filePaths)
    {
        // 实现自定义文件分类逻辑
    }
    
    public async Task<string> GenerateFileName(string filePath)
    {
        // 实现自定义文件名生成逻辑
    }
    
    public async Task<string> GetCleaningSuggestions(string diskPath)
    {
        // 实现自定义清理建议逻辑
    }
    
    public bool IsAvailable()
    {
        // 检查服务是否可用
    }
}
```

### 5.2 切换AI服务

使用AIServiceFactory切换到自定义AI服务：

```csharp
// 设置自定义AI服务
AIServiceFactory.SetAIService(new CustomAIService());

// 获取服务实例（现在返回的是自定义服务）
var aiService = AIServiceFactory.GetAIService();
```

## 6. 性能优化

### 6.1 内存优化

- **延迟加载**：只在需要时初始化AI服务
- **资源释放**：使用using语句确保资源正确释放
- **批处理**：批量处理文件，减少API调用次数

### 6.2 缓存策略

- **结果缓存**：缓存频繁使用的分析结果
- **文件类型缓存**：缓存常见文件类型的分类结果
- **清理建议缓存**：缓存磁盘清理建议，定期更新

## 7. 最佳实践

### 7.1 错误处理

```csharp
try
{
    var aiService = AIServiceFactory.GetAIService();
    if (aiService.IsAvailable())
    {
        // 执行AI操作
    }
    else
    {
        // 处理服务不可用的情况
    }
}
catch (Exception ex)
{
    // 记录错误并提供备用方案
    Console.WriteLine($"AI服务错误: {ex.Message}");
    // 使用备用逻辑
}
```

### 7.2 异步操作

```csharp
// 使用异步方法避免阻塞UI线程
private async void AnalyzeButton_Click(object sender, RoutedEventArgs e)
{
    try
    {
        // 显示加载指示器
        loadingIndicator.Visibility = Visibility.Visible;
        
        // 执行异步AI操作
        var aiService = AIServiceFactory.GetAIService();
        string analysis = await aiService.AnalyzeFile(filePathTextBox.Text);
        
        // 显示结果
        resultTextBlock.Text = analysis;
    }
    finally
    {
        // 隐藏加载指示器
        loadingIndicator.Visibility = Visibility.Collapsed;
    }
}
```

### 7.3 混合使用策略

- **本地优先**：优先使用MLNetAIService处理简单任务
- **云服务备用**：对于复杂任务，使用云AI服务
- **智能切换**：根据任务复杂度和系统资源自动选择服务

## 8. 测试指南

### 8.1 单元测试

```csharp
[TestClass]
public class AIServiceTests
{
    [TestMethod]
    public async Task AnalyzeFile_ValidPath_ReturnsAnalysis()
    {
        // 准备测试文件
        string testFile = Path.Combine(Path.GetTempPath(), "test.txt");
        File.WriteAllText(testFile, "Test content");
        
        // 获取AI服务
        var aiService = AIServiceFactory.GetAIService();
        
        // 执行测试
        string result = await aiService.AnalyzeFile(testFile);
        
        // 验证结果
        Assert.IsNotNull(result);
        Assert.Contains(".txt", result);
        
        // 清理测试文件
        File.Delete(testFile);
    }
}
```

### 8.2 性能测试

- **内存使用**：监控AI服务的内存占用
- **响应时间**：测试不同大小文件的分析时间
- **并发性能**：测试多线程同时调用AI服务的性能

## 9. 未来扩展

### 9.1 增强ML.NET模型

- **训练自定义模型**：使用用户数据训练更准确的文件分类模型
- **模型优化**：针对特定文件类型优化模型性能
- **增量学习**：根据用户反馈不断改进模型

### 9.2 集成云AI服务

- **Azure OpenAI**：集成Azure OpenAI服务以提供更高级的AI功能
- **OpenAI API**：集成OpenAI API以使用最新的GPT模型
- **成本控制**：实现智能切换机制，平衡成本和性能

### 9.3 高级功能

- **文件内容分析**：分析文件内容以提供更准确的分类和建议
- **用户行为学习**：学习用户的文件管理习惯，提供个性化建议
- **预测性分析**：预测磁盘空间使用趋势，提前提供清理建议

## 10. 总结

本AI服务架构设计灵活、可扩展，既可以使用本地ML.NET实现零成本运行，又可以通过扩展接口集成云AI服务以获得更强大的功能。通过遵循本开发指令，可以确保AI功能的性能、可靠性和可扩展性，为用户提供智能、高效的磁盘清理与数据治理体验。