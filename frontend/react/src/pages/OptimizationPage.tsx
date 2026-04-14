import React, { useState } from 'react';

const OptimizationPage: React.FC = () => {
  const [startupItems, setStartupItems] = useState([
    { id: '1', name: 'Chrome', path: 'C:\\Program Files\\Google\\Chrome\\chrome.exe', enabled: true, impact: 'medium' },
    { id: '2', name: 'Discord', path: 'C:\\Program Files\\Discord\\Discord.exe', enabled: true, impact: 'low' },
    { id: '3', name: 'Steam', path: 'C:\\Program Files (x86)\\Steam\\steam.exe', enabled: true, impact: 'high' },
    { id: '4', name: 'OneDrive', path: 'C:\\Program Files\\Microsoft OneDrive\\OneDrive.exe', enabled: true, impact: 'medium' },
    { id: '5', name: 'Spotify', path: 'C:\\Program Files\\Spotify\\Spotify.exe', enabled: false, impact: 'low' },
  ]);

  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optimizationProgress, setOptimizationProgress] = useState(0);

  const toggleStartupItem = (id: string) => {
    setStartupItems(prev => prev.map(item => 
      item.id === id ? { ...item, enabled: !item.enabled } : item
    ));
  };

  const startOptimization = () => {
    setIsOptimizing(true);
    setOptimizationProgress(0);
    
    // 模拟优化过程
    const interval = setInterval(() => {
      setOptimizationProgress(prev => {
        const newProgress = prev + 10;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsOptimizing(false);
          // 模拟优化完成
          alert('系统优化完成！');
          return 100;
        }
        return newProgress;
      });
    }, 300);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">系统优化</h1>
        <p className="text-gray-600 mb-6">管理启动项，清理注册表，优化系统性能</p>
      </div>

      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">系统优化</h3>
          <button 
            className="btn btn-primary" 
            onClick={startOptimization}
            disabled={isOptimizing}
          >
            {isOptimizing ? '优化中...' : '开始优化'}
          </button>
        </div>
        {isOptimizing && (
          <div className="space-y-2">
            <div className="progress-bar">
              <div 
                className="progress-bar-fill bg-primary" 
                style={{ width: `${optimizationProgress}%` }}
              ></div>
            </div>
            <div className="flex justify-between text-sm">
              <span>优化进度</span>
              <span>{optimizationProgress}%</span>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">启动项管理</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">启用</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">名称</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">路径</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">启动影响</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {startupItems.map((item) => (
                <tr key={item.id}>
                  <td className="px-4 py-3">
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input 
                        type="checkbox" 
                        checked={item.enabled} 
                        onChange={() => toggleStartupItem(item.id)}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                    </label>
                  </td>
                  <td className="px-4 py-3 text-sm font-medium">{item.name}</td>
                  <td className="px-4 py-3 text-sm text-gray-600 truncate w-64">{item.path}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      item.impact === 'high' ? 'bg-red-100 text-red-800' :
                      item.impact === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {item.impact === 'high' ? '高' :
                       item.impact === 'medium' ? '中' :
                       '低'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">注册表清理</h3>
        <p className="text-gray-600 mb-4">清理无效的注册表项，优化系统性能</p>
        <button className="btn btn-primary w-full">
          清理注册表
        </button>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">系统信息</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">操作系统</p>
            <p className="font-medium">Windows 11 Pro 22H2</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">处理器</p>
            <p className="font-medium">Intel Core i7-11700K</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">内存</p>
            <p className="font-medium">16 GB DDR4 3200MHz</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">系统盘</p>
            <p className="font-medium">C: 1TB NVMe SSD</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OptimizationPage;