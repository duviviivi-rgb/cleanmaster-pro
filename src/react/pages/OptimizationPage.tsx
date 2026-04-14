import React, { useState } from 'react';

const OptimizationPage: React.FC = () => {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [optimizationType, setOptimizationType] = useState<'quick' | 'standard' | 'deep'>('standard');
  const [optimizationResult, setOptimizationResult] = useState<any>(null);

  const startOptimization = () => {
    setIsOptimizing(true);
    setProgress(0);
    
    // 模拟优化过程
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsOptimizing(false);
          // 模拟优化结果
          setOptimizationResult({
            startupTime: '10.5s',
            memorySaved: 512000000,
            performanceScore: 85,
            message: '系统优化完成'
          });
          return 100;
        }
        return prev + 10;
      });
    }, 300);
  };

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">系统优化</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">选择优化类型</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <button 
            onClick={() => setOptimizationType('quick')}
            className={`p-4 rounded-lg border ${optimizationType === 'quick' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">快速优化</h3>
            <p className="text-sm text-gray-600">优化启动项和服务</p>
          </button>
          <button 
            onClick={() => setOptimizationType('standard')}
            className={`p-4 rounded-lg border ${optimizationType === 'standard' ? 'border-purple-500 bg-purple-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">标准优化</h3>
            <p className="text-sm text-gray-600">全面系统性能优化</p>
          </button>
          <button 
            onClick={() => setOptimizationType('deep')}
            className={`p-4 rounded-lg border ${optimizationType === 'deep' ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">深度优化</h3>
            <p className="text-sm text-gray-600">高级系统配置优化</p>
          </button>
        </div>
        
        <button 
          onClick={startOptimization}
          disabled={isOptimizing}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
        >
          {isOptimizing ? '优化中...' : '开始优化'}
        </button>
      </div>

      {isOptimizing && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">优化进度</h2>
          <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
            <div 
              className="bg-blue-600 h-4 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="flex justify-between text-sm">
            <span>正在执行 {optimizationType === 'quick' ? '快速' : optimizationType === 'standard' ? '标准' : '深度'} 优化</span>
            <span>{progress}%</span>
          </div>
        </div>
      )}

      {optimizationResult && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">优化结果</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <div className="text-gray-500 text-sm">启动时间</div>
              <div className="font-medium">{optimizationResult.startupTime}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">释放内存</div>
              <div className="font-medium text-green-600">{formatBytes(optimizationResult.memorySaved)}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">性能评分</div>
              <div className="font-medium">{optimizationResult.performanceScore}/100</div>
            </div>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
            <div 
              className="bg-green-600 h-4 rounded-full"
              style={{ width: `${optimizationResult.performanceScore}%` }}
            ></div>
          </div>
          
          <div className="mt-4">
            <p className="text-green-600">{optimizationResult.message}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default OptimizationPage;