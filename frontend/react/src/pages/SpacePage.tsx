import React, { useState } from 'react';

const SpacePage: React.FC = () => {
  const [selectedDisk, setSelectedDisk] = useState('C:');
  const [spaceUsage] = useState({
    totalSpace: 1000000000000,
    usedSpace: 600000000000,
    freeSpace: 400000000000,
    fileTypes: [
      { type: '文档', size: 100000000000 },
      { type: '图片', size: 150000000000 },
      { type: '视频', size: 200000000000 },
      { type: '应用', size: 100000000000 },
      { type: '其他', size: 50000000000 },
    ],
    largeFiles: [
      { name: 'installer.exe', path: 'C:\\Downloads\\installer.exe', size: 5000000000 },
      { name: 'movie.mp4', path: 'C:\\Videos\\movie.mp4', size: 3500000000 },
      { name: 'game.iso', path: 'C:\\Games\\game.iso', size: 8000000000 },
      { name: 'backup.zip', path: 'C:\\Backups\\backup.zip', size: 6000000000 },
      { name: 'database.mdb', path: 'C:\\Data\\database.mdb', size: 2500000000 },
    ],
    topDirectories: [
      { name: 'Users', path: 'C:\\Users', size: 300000000000 },
      { name: 'Program Files', path: 'C:\\Program Files', size: 150000000000 },
      { name: 'Windows', path: 'C:\\Windows', size: 100000000000 },
      { name: 'Downloads', path: 'C:\\Downloads', size: 30000000000 },
      { name: 'Documents', path: 'C:\\Documents', size: 20000000000 },
    ],
  });

  const disks = [
    { letter: 'C:', name: '系统盘', totalSpace: 1000000000000, usedSpace: 600000000000 },
    { letter: 'D:', name: '数据盘', totalSpace: 2000000000000, usedSpace: 1200000000000 },
    { letter: 'E:', name: '娱乐盘', totalSpace: 1500000000000, usedSpace: 800000000000 },
  ];

  const formatSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">空间管理</h1>
        <p className="text-gray-600 mb-6">分析磁盘空间使用情况，识别大文件和占用空间较大的目录</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {disks.map((disk) => {
          const usedPercentage = (disk.usedSpace / disk.totalSpace) * 100;
          return (
            <div 
              key={disk.letter} 
              className={`card cursor-pointer transition-all duration-300 ${
                selectedDisk === disk.letter ? 'border-2 border-primary' : ''
              }`}
              onClick={() => setSelectedDisk(disk.letter)}
            >
              <h3 className="text-lg font-semibold mb-2">{disk.letter} {disk.name}</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>已用空间</span>
                  <span>{formatSize(disk.usedSpace)} / {formatSize(disk.totalSpace)}</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-bar-fill bg-primary" 
                    style={{ width: `${usedPercentage}%` }}
                  ></div>
                </div>
                <div className="flex justify-end text-sm font-medium">
                  {usedPercentage.toFixed(1)}%
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">空间使用情况</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">总空间</p>
            <p className="text-2xl font-bold">{formatSize(spaceUsage.totalSpace)}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">已用空间</p>
            <p className="text-2xl font-bold text-primary">{formatSize(spaceUsage.usedSpace)}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">可用空间</p>
            <p className="text-2xl font-bold text-success">{formatSize(spaceUsage.freeSpace)}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">文件类型分布</h3>
          <div className="space-y-3">
            {spaceUsage.fileTypes.map((fileType, index) => (
              <div key={index}>
                <div className="flex justify-between text-sm mb-1">
                  <span>{fileType.type}</span>
                  <span>{formatSize(fileType.size)}</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-bar-fill bg-secondary" 
                    style={{ 
                      width: `${(fileType.size / spaceUsage.usedSpace) * 100}%` 
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">大文件</h3>
          <div className="space-y-3">
            {spaceUsage.largeFiles.map((file, index) => (
              <div key={index} className="flex items-center justify-between p-2 border-b border-gray-100">
                <div>
                  <p className="font-medium">{file.name}</p>
                  <p className="text-xs text-gray-600 truncate w-48">{file.path}</p>
                </div>
                <span className="text-sm font-medium text-primary">{formatSize(file.size)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">占用空间较大的目录</h3>
        <div className="space-y-3">
          {spaceUsage.topDirectories.map((dir, index) => (
            <div key={index} className="flex items-center justify-between p-2 border-b border-gray-100">
              <div>
                <p className="font-medium">{dir.name}</p>
                <p className="text-xs text-gray-600 truncate w-64">{dir.path}</p>
              </div>
              <span className="text-sm font-medium text-primary">{formatSize(dir.size)}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">空间趋势</h3>
        <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <p className="text-gray-500">空间趋势图表</p>
        </div>
      </div>
    </div>
  );
};

export default SpacePage;