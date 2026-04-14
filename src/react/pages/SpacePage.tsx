import React, { useState } from 'react';

const SpacePage: React.FC = () => {
  const [selectedDisk, setSelectedDisk] = useState('C:');
  
  // 模拟磁盘数据
  const diskData = {
    'C:': {
      totalSpace: 135000000000,
      usedSpace: 100000000000,
      freeSpace: 35000000000,
      percentage: 74,
      topDirectories: [
        { name: 'Windows', size: 40000000000, percentage: 40 },
        { name: 'Program Files', size: 20000000000, percentage: 20 },
        { name: 'Users', size: 25000000000, percentage: 25 },
        { name: 'ProgramData', size: 10000000000, percentage: 10 },
        { name: '其他', size: 5000000000, percentage: 5 }
      ],
      fileTypes: [
        { type: '系统文件', size: 45000000000, percentage: 45 },
        { type: '应用程序', size: 25000000000, percentage: 25 },
        { type: '文档', size: 15000000000, percentage: 15 },
        { type: '媒体文件', size: 10000000000, percentage: 10 },
        { type: '其他', size: 5000000000, percentage: 5 }
      ]
    },
    'D:': {
      totalSpace: 500000000000,
      usedSpace: 200000000000,
      freeSpace: 300000000000,
      percentage: 40,
      topDirectories: [
        { name: 'Movies', size: 80000000000, percentage: 40 },
        { name: 'Music', size: 40000000000, percentage: 20 },
        { name: 'Documents', size: 60000000000, percentage: 30 },
        { name: 'Other', size: 20000000000, percentage: 10 }
      ],
      fileTypes: [
        { type: '视频', size: 80000000000, percentage: 40 },
        { type: '音频', size: 40000000000, percentage: 20 },
        { type: '文档', size: 60000000000, percentage: 30 },
        { type: '其他', size: 20000000000, percentage: 10 }
      ]
    },
    'E:': {
      totalSpace: 250000000000,
      usedSpace: 180000000000,
      freeSpace: 70000000000,
      percentage: 72,
      topDirectories: [
        { name: 'Games', size: 120000000000, percentage: 67 },
        { name: 'Software', size: 40000000000, percentage: 22 },
        { name: 'Other', size: 20000000000, percentage: 11 }
      ],
      fileTypes: [
        { type: '游戏文件', size: 120000000000, percentage: 67 },
        { type: '安装程序', size: 40000000000, percentage: 22 },
        { type: '其他', size: 20000000000, percentage: 11 }
      ]
    }
  };

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

  const currentDisk = diskData[selectedDisk as keyof typeof diskData];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">空间管理</h1>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">选择磁盘</label>
        <select 
          value={selectedDisk}
          onChange={(e) => setSelectedDisk(e.target.value)}
          className="w-32 px-3 py-2 border border-gray-300 rounded-md"
        >
          <option value="C:">C: 系统盘</option>
          <option value="D:">D: 数据盘</option>
          <option value="E:">E: 游戏盘</option>
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">磁盘空间概览</h2>
          <div className="w-full bg-gray-200 rounded-full h-8 mb-4">
            <div 
              className={`h-8 rounded-full ${getProgressColor(currentDisk.percentage)} transition-all duration-300`}
              style={{ width: `${currentDisk.percentage}%` }}
            ></div>
          </div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-gray-500 text-sm">总空间</div>
              <div className="font-medium">{formatBytes(currentDisk.totalSpace)}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">已用空间</div>
              <div className="font-medium">{formatBytes(currentDisk.usedSpace)}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">可用空间</div>
              <div className="font-medium text-green-600">{formatBytes(currentDisk.freeSpace)}</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">文件类型分布</h2>
          <div className="space-y-3">
            {currentDisk.fileTypes.map((type: any, index: number) => (
              <div key={index}>
                <div className="flex justify-between mb-1">
                  <span>{type.type}</span>
                  <span>{formatBytes(type.size)} ({type.percentage}%)</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${type.percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 lg:col-span-2">
          <h2 className="text-lg font-semibold mb-4">占用空间最多的目录</h2>
          <div className="space-y-3">
            {currentDisk.topDirectories.map((dir: any, index: number) => (
              <div key={index} className="flex items-center">
                <div className="w-1/3">
                  <span className="font-medium">{dir.name}</span>
                </div>
                <div className="w-1/2 mx-4">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-purple-600 h-2 rounded-full"
                      style={{ width: `${dir.percentage}%` }}
                    ></div>
                  </div>
                </div>
                <div className="w-1/6 text-right">
                  <span>{formatBytes(dir.size)}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpacePage;