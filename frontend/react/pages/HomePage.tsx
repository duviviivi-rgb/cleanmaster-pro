import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  // 模拟磁盘数据
  const disks = [
    {
      letter: 'C:',
      name: '系统盘',
      totalSpace: 135000000000,
      usedSpace: 100000000000,
      freeSpace: 35000000000,
      percentage: 74
    },
    {
      letter: 'D:',
      name: '数据盘',
      totalSpace: 500000000000,
      usedSpace: 200000000000,
      freeSpace: 300000000000,
      percentage: 40
    },
    {
      letter: 'E:',
      name: '游戏盘',
      totalSpace: 250000000000,
      usedSpace: 180000000000,
      freeSpace: 70000000000,
      percentage: 72
    }
  ];

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getProgressColor = (percentage: number): string => {
    if (percentage < 50) return 'bg-green-500';
    if (percentage < 80) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">磁盘概览</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {disks.map((disk) => (
          <div key={disk.letter} className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">{disk.letter} {disk.name}</h2>
              <span className={`text-sm font-medium ${disk.percentage > 80 ? 'text-red-500' : disk.percentage > 50 ? 'text-yellow-500' : 'text-green-500'}`}>
                {disk.percentage}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
              <div 
                className={`h-2.5 rounded-full ${getProgressColor(disk.percentage)}`}
                style={{ width: `${disk.percentage}%` }}
              ></div>
            </div>
            <div className="grid grid-cols-3 gap-2 text-sm">
              <div>
                <div className="text-gray-500">总空间</div>
                <div className="font-medium">{formatBytes(disk.totalSpace)}</div>
              </div>
              <div>
                <div className="text-gray-500">已用空间</div>
                <div className="font-medium">{formatBytes(disk.usedSpace)}</div>
              </div>
              <div>
                <div className="text-gray-500">可用空间</div>
                <div className="font-medium">{formatBytes(disk.freeSpace)}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <h2 className="text-xl font-bold mb-4">快速操作</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <button 
          onClick={() => navigate('/scan')}
          className="bg-blue-600 text-white p-6 rounded-lg shadow hover:bg-blue-700 transition-colors flex flex-col items-center justify-center"
        >
          <span className="text-3xl mb-2">🔍</span>
          <span className="font-medium">快速扫描</span>
        </button>
        <button 
          onClick={() => navigate('/scan')}
          className="bg-purple-600 text-white p-6 rounded-lg shadow hover:bg-purple-700 transition-colors flex flex-col items-center justify-center"
        >
          <span className="text-3xl mb-2">🔬</span>
          <span className="font-medium">深度扫描</span>
        </button>
        <button 
          onClick={() => navigate('/clean')}
          className="bg-green-600 text-white p-6 rounded-lg shadow hover:bg-green-700 transition-colors flex flex-col items-center justify-center"
        >
          <span className="text-3xl mb-2">🧹</span>
          <span className="font-medium">执行清理</span>
        </button>
        <button 
          onClick={() => navigate('/space')}
          className="bg-amber-600 text-white p-6 rounded-lg shadow hover:bg-amber-700 transition-colors flex flex-col items-center justify-center"
        >
          <span className="text-3xl mb-2">📊</span>
          <span className="font-medium">空间分析</span>
        </button>
      </div>
    </div>
  );
};

export default HomePage;