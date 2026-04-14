import React, { useState } from 'react';

const CleanPage: React.FC = () => {
  const [isCleaning, setIsCleaning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [cleanResults, setCleanResults] = useState({
    spaceSaved: 0,
    filesDeleted: 0,
  });
  const [autoCleanEnabled, setAutoCleanEnabled] = useState(false);
  const [cleanSchedule, setCleanSchedule] = useState('daily');
  const [cleanLevel, setCleanLevel] = useState('standard');

  const formatSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const startClean = () => {
    setIsCleaning(true);
    setProgress(0);
    
    // 模拟清理过程
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 5;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsCleaning(false);
          // 模拟清理结果
          setCleanResults({
            spaceSaved: 25000000000, // 25GB
            filesDeleted: 3200,
          });
          return 100;
        }
        return newProgress;
      });
    }, 200);
  };

  const stopClean = () => {
    setIsCleaning(false);
    setProgress(0);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">清理</h1>
        <p className="text-gray-600 mb-6">执行清理操作，释放磁盘空间</p>
      </div>

      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">清理操作</h3>
          <div className="flex space-x-2">
            {isCleaning ? (
              <button className="btn btn-danger" onClick={stopClean}>
                停止
              </button>
            ) : (
              <button className="btn btn-primary" onClick={startClean}>
                开始清理
              </button>
            )}
          </div>
        </div>
        <div className="space-y-4">
          <div className="progress-bar">
            <div 
              className="progress-bar-fill bg-primary" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="flex justify-between text-sm">
            <span>清理进度</span>
            <span>{progress}%</span>
          </div>
          {isCleaning && (
            <div className="text-sm text-gray-600">
              正在清理... 已删除 {Math.floor(progress * 32)} 个文件
            </div>
          )}
        </div>
      </div>

      {!isCleaning && progress === 100 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">清理结果</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">节省空间</p>
              <p className="text-2xl font-bold text-primary">{formatSize(cleanResults.spaceSaved)}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">删除文件数</p>
              <p className="text-2xl font-bold">{cleanResults.filesDeleted.toLocaleString()}</p>
            </div>
          </div>
          <div className="flex space-x-2">
            <button className="btn btn-secondary flex-1">
              查看详情
            </button>
            <button className="btn btn-primary flex-1">
              再次清理
            </button>
          </div>
        </div>
      )}

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">自动清理设置</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span>启用自动清理</span>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                checked={autoCleanEnabled} 
                onChange={() => setAutoCleanEnabled(!autoCleanEnabled)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
            </label>
          </div>
          {autoCleanEnabled && (
            <div className="space-y-4 pl-4 border-l-2 border-gray-100">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">清理频率</label>
                <select 
                  value={cleanSchedule} 
                  onChange={(e) => setCleanSchedule(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="daily">每天</option>
                  <option value="weekly">每周</option>
                  <option value="monthly">每月</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">清理级别</label>
                <select 
                  value={cleanLevel} 
                  onChange={(e) => setCleanLevel(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  <option value="quick">快速清理</option>
                  <option value="standard">标准清理</option>
                  <option value="deep">深度清理</option>
                </select>
              </div>
              <button className="btn btn-primary w-full">
                保存设置
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">批量清理</h3>
        <p className="text-gray-600 mb-4">选择要清理的磁盘，点击开始按钮进行批量清理</p>
        <div className="space-y-2 mb-4">
          <div className="flex items-center">
            <input type="checkbox" className="mr-2" />
            <span>C: 系统盘</span>
          </div>
          <div className="flex items-center">
            <input type="checkbox" className="mr-2" />
            <span>D: 数据盘</span>
          </div>
          <div className="flex items-center">
            <input type="checkbox" className="mr-2" />
            <span>E: 娱乐盘</span>
          </div>
        </div>
        <button className="btn btn-primary w-full">
          开始批量清理
        </button>
      </div>
    </div>
  );
};

export default CleanPage;