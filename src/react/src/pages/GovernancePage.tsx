import React, { useState } from 'react';

const GovernancePage: React.FC = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [fileCategories, setFileCategories] = useState([
    { name: '文档', count: 120, size: 5000000000, growthRate: 10000000 },
    { name: '图片', count: 500, size: 10000000000, growthRate: 20000000 },
    { name: '视频', count: 50, size: 20000000000, growthRate: 50000000 },
    { name: '音频', count: 200, size: 2000000000, growthRate: 5000000 },
    { name: '应用', count: 30, size: 15000000000, growthRate: 15000000 },
    { name: '其他', count: 800, size: 8000000000, growthRate: 8000000 },
  ]);
  const [duplicateFiles, setDuplicateFiles] = useState([
    { groupId: '1', files: ['C:\\Documents\\file1.docx', 'C:\\Downloads\\file1_copy.docx'], size: 2000000 },
    { groupId: '2', files: ['C:\\Pictures\\photo1.jpg', 'C:\\Backup\\photo1_copy.jpg'], size: 5000000 },
    { groupId: '3', files: ['C:\\Videos\\video1.mp4', 'C:\\Movies\\video1_copy.mp4'], size: 50000000 },
  ]);

  const formatSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const startAnalysis = () => {
    setIsAnalyzing(true);
    setAnalysisProgress(0);
    
    // 模拟分析过程
    const interval = setInterval(() => {
      setAnalysisProgress(prev => {
        const newProgress = prev + 5;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsAnalyzing(false);
          return 100;
        }
        return newProgress;
      });
    }, 200);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">数据治理</h1>
        <p className="text-gray-600 mb-6">分析文件分类，检测重复文件，优化数据结构</p>
      </div>

      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">分析文件分类</h3>
          <button 
            className="btn btn-primary" 
            onClick={startAnalysis}
            disabled={isAnalyzing}
          >
            {isAnalyzing ? '分析中...' : '开始分析'}
          </button>
        </div>
        {isAnalyzing && (
          <div className="space-y-2">
            <div className="progress-bar">
              <div 
                className="progress-bar-fill bg-primary" 
                style={{ width: `${analysisProgress}%` }}
              ></div>
            </div>
            <div className="flex justify-between text-sm">
              <span>分析进度</span>
              <span>{analysisProgress}%</span>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">文件分类分析</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">分类</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">文件数</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">大小</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">日增长率</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {fileCategories.map((category, index) => (
                <tr key={index}>
                  <td className="px-4 py-3 text-sm font-medium">{category.name}</td>
                  <td className="px-4 py-3 text-sm">{category.count.toLocaleString()}</td>
                  <td className="px-4 py-3 text-sm">{formatSize(category.size)}</td>
                  <td className="px-4 py-3 text-sm">{formatSize(category.growthRate)}</td>
                  <td className="px-4 py-3 text-sm">
                    <button className="text-primary hover:underline">查看</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">重复文件检测</h3>
        <div className="space-y-4">
          {duplicateFiles.map((group) => (
            <div key={group.groupId} className="border-b border-gray-100 pb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">重复文件组 #{group.groupId}</span>
                <span className="text-sm text-primary">{formatSize(group.size)}</span>
              </div>
              <div className="space-y-1">
                {group.files.map((file, index) => (
                  <div key={index} className="text-sm text-gray-600 truncate">{file}</div>
                ))}
              </div>
              <div className="mt-2 flex space-x-2">
                <button className="btn btn-secondary text-xs">
                  保留一个
                </button>
                <button className="btn btn-danger text-xs">
                  删除重复
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">数据结构优化</h3>
        <p className="text-gray-600 mb-4">优化文件结构，符合AI管理逻辑，提高文件组织效率</p>
        <button className="btn btn-primary w-full">
          优化数据结构
        </button>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">数据备份</h3>
        <p className="text-gray-600 mb-4">备份重要数据，确保数据安全</p>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">备份路径</label>
            <input 
              type="text" 
              className="w-full p-2 border border-gray-300 rounded-md" 
              defaultValue="D:\\Backup"
            />
          </div>
          <button className="btn btn-primary w-full">
            开始备份
          </button>
        </div>
      </div>
    </div>
  );
};

export default GovernancePage;