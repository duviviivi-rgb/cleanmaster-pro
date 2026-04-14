import React, { useState } from 'react';

const GovernancePage: React.FC = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [analysisResults, setAnalysisResults] = useState<any>(null);

  const startAnalysis = () => {
    setIsAnalyzing(true);
    setProgress(0);
    
    // 模拟分析过程
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsAnalyzing(false);
          // 模拟分析结果
          setAnalysisResults({
            totalFiles: 15000,
            uncategorized: 3000,
            categories: [
              { name: '文档', count: 5000, percentage: 33.3 },
              { name: '图片', count: 3000, percentage: 20 },
              { name: '视频', count: 2000, percentage: 13.3 },
              { name: '音频', count: 1000, percentage: 6.7 },
              { name: '其他', count: 1000, percentage: 6.7 }
            ]
          });
          return 100;
        }
        return prev + 10;
      });
    }, 300);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">数据治理</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">文件分类分析</h2>
        <p className="text-gray-600 mb-6">分析文件结构，提供智能归类建议</p>
        
        <button 
          onClick={startAnalysis}
          disabled={isAnalyzing}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
        >
          {isAnalyzing ? '分析中...' : '开始分析'}
        </button>
      </div>

      {isAnalyzing && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">分析进度</h2>
          <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
            <div 
              className="bg-blue-600 h-4 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="flex justify-between text-sm">
            <span>正在分析文件结构</span>
            <span>{progress}%</span>
          </div>
        </div>
      )}

      {analysisResults && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">分析结果</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <div className="text-gray-500 text-sm">总文件数</div>
              <div className="font-medium">{analysisResults.totalFiles}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">未分类文件</div>
              <div className="font-medium text-amber-600">{analysisResults.uncategorized}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">分类率</div>
              <div className="font-medium">{Math.round((1 - analysisResults.uncategorized / analysisResults.totalFiles) * 100)}%</div>
            </div>
          </div>
          
          <h3 className="font-medium mb-3">文件分类分布</h3>
          <div className="space-y-3">
            {analysisResults.categories.map((category: any, index: number) => (
              <div key={index}>
                <div className="flex justify-between mb-1">
                  <span>{category.name}</span>
                  <span>{category.count} ({category.percentage.toFixed(1)}%)</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-purple-600 h-2 rounded-full"
                    style={{ width: `${category.percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-6">
            <button className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors">
              执行智能归类
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GovernancePage;