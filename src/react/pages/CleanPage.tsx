import React, { useState } from 'react';

const CleanPage: React.FC = () => {
  const [isCleaning, setIsCleaning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [cleanType, setCleanType] = useState<'quick' | 'standard' | 'deep'>('standard');
  const [autoCleanEnabled, setAutoCleanEnabled] = useState(false);
  const [cleanSchedule, setCleanSchedule] = useState('0 2 * * 0'); // 每周日凌晨2点
  const [cleanLevel, setCleanLevel] = useState<'quick' | 'standard' | 'deep'>('standard');
  const [cleanResult, setCleanResult] = useState<any>(null);

  const startClean = () => {
    setIsCleaning(true);
    setProgress(0);
    
    // 模拟清理过程
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsCleaning(false);
          // 模拟清理结果
          setCleanResult({
            spaceSaved: 2500000000,
            filesDeleted: 150,
            message: '清理完成'
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
      <h1 className="text-2xl font-bold mb-6">清理</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">执行清理</h2>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">清理级别</label>
            <div className="space-y-2">
              <div className="flex items-center">
                <input 
                  type="radio" 
                  id="quick" 
                  name="cleanType" 
                  value="quick" 
                  checked={cleanType === 'quick'}
                  onChange={() => setCleanType('quick')}
                  className="mr-2"
                />
                <label htmlFor="quick">快速清理</label>
              </div>
              <div className="flex items-center">
                <input 
                  type="radio" 
                  id="standard" 
                  name="cleanType" 
                  value="standard" 
                  checked={cleanType === 'standard'}
                  onChange={() => setCleanType('standard')}
                  className="mr-2"
                />
                <label htmlFor="standard">标准清理</label>
              </div>
              <div className="flex items-center">
                <input 
                  type="radio" 
                  id="deep" 
                  name="cleanType" 
                  value="deep" 
                  checked={cleanType === 'deep'}
                  onChange={() => setCleanType('deep')}
                  className="mr-2"
                />
                <label htmlFor="deep">深度清理</label>
              </div>
            </div>
          </div>
          
          <button 
            onClick={startClean}
            disabled={isCleaning}
            className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400"
          >
            {isCleaning ? '清理中...' : '开始清理'}
          </button>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">自动清理</h2>
          
          <div className="mb-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">启用自动清理</label>
              <label className="relative inline-flex items-center cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={autoCleanEnabled}
                  onChange={(e) => setAutoCleanEnabled(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
          
          {autoCleanEnabled && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">定时规则 (Cron)</label>
                <input 
                  type="text" 
                  value={cleanSchedule}
                  onChange={(e) => setCleanSchedule(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="0 2 * * 0"
                />
                <p className="text-xs text-gray-500 mt-1">格式: 分 时 日 月 周</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">清理级别</label>
                <select 
                  value={cleanLevel}
                  onChange={(e) => setCleanLevel(e.target.value as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="quick">快速清理</option>
                  <option value="standard">标准清理</option>
                  <option value="deep">深度清理</option>
                </select>
              </div>
              
              <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                保存设置
              </button>
            </div>
          )}
        </div>
      </div>

      {isCleaning && (
        <div className="mt-6 bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">清理进度</h2>
          <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
            <div 
              className="bg-green-600 h-4 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="flex justify-between text-sm">
            <span>正在执行 {cleanType === 'quick' ? '快速' : cleanType === 'standard' ? '标准' : '深度'} 清理</span>
            <span>{progress}%</span>
          </div>
        </div>
      )}

      {cleanResult && (
        <div className="mt-6 bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">清理结果</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div className="text-gray-500 text-sm">节省空间</div>
              <div className="font-medium text-green-600">{formatBytes(cleanResult.spaceSaved)}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">删除文件数</div>
              <div className="font-medium">{cleanResult.filesDeleted}</div>
            </div>
          </div>
          <div className="mt-4">
            <p className="text-green-600">{cleanResult.message}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CleanPage;