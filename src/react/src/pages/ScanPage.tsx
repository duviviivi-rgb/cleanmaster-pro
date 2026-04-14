import React, { useState } from 'react';

const ScanPage: React.FC = () => {
  const [scanType, setScanType] = useState('quick');
  const [isScanning, setIsScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [scanResults, setScanResults] = useState({
    totalFiles: 0,
    cleanableFiles: 0,
    cleanableSpace: 0,
    fileTypes: [] as { type: string; count: number; size: number }[],
  });

  const scanTypes = [
    { value: 'quick', label: '快速扫描', description: '扫描临时文件和缓存' },
    { value: 'deep', label: '深度扫描', description: '全面扫描所有可清理文件' },
    { value: 'incremental', label: '增量扫描', description: '只扫描上次扫描后变化的文件' },
    { value: 'smart', label: '智能分析', description: '基于AI的智能扫描和分析' },
  ];

  const formatSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const startScan = () => {
    setIsScanning(true);
    setProgress(0);
    
    // 模拟扫描过程
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 5;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsScanning(false);
          // 模拟扫描结果
          setScanResults({
            totalFiles: 12500,
            cleanableFiles: 3200,
            cleanableSpace: 25000000000, // 25GB
            fileTypes: [
              { type: '临时文件', count: 1500, size: 10000000000 },
              { type: '浏览器缓存', count: 800, size: 8000000000 },
              { type: '日志文件', count: 400, size: 3000000000 },
              { type: '安装包', count: 200, size: 4000000000 },
            ],
          });
          return 100;
        }
        return newProgress;
      });
    }, 200);
  };

  const stopScan = () => {
    setIsScanning(false);
    setProgress(0);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">扫描</h1>
        <p className="text-gray-600 mb-6">选择扫描类型，点击开始按钮进行扫描</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {scanTypes.map((type) => (
          <div
            key={type.value}
            className={`card cursor-pointer transition-all duration-300 ${
              scanType === type.value ? 'border-2 border-primary' : ''
            }`}
            onClick={() => setScanType(type.value)}
          >
            <h3 className="text-lg font-semibold mb-2">{type.label}</h3>
            <p className="text-sm text-gray-600 mb-4">{type.description}</p>
            {scanType === type.value && (
              <div className="w-full h-1 bg-primary rounded-full"></div>
            )}
          </div>
        ))}
      </div>

      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">扫描进度</h3>
          <div className="flex space-x-2">
            {isScanning ? (
              <button className="btn btn-danger" onClick={stopScan}>
                停止
              </button>
            ) : (
              <button className="btn btn-primary" onClick={startScan}>
                开始扫描
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
            <span>扫描进度</span>
            <span>{progress}%</span>
          </div>
          {isScanning && (
            <div className="text-sm text-gray-600">
              正在扫描... 已扫描 {Math.floor(progress * 125)} 个文件
            </div>
          )}
        </div>
      </div>

      {!isScanning && progress === 100 && (
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">扫描结果</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">总文件数</p>
              <p className="text-2xl font-bold">{scanResults.totalFiles.toLocaleString()}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">可清理文件</p>
              <p className="text-2xl font-bold">{scanResults.cleanableFiles.toLocaleString()}</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600">可节省空间</p>
              <p className="text-2xl font-bold text-primary">{formatSize(scanResults.cleanableSpace)}</p>
            </div>
          </div>
          <div className="space-y-4">
            <h4 className="font-semibold">文件类型分布</h4>
            <div className="space-y-2">
              {scanResults.fileTypes.map((fileType, index) => (
                <div key={index}>
                  <div className="flex justify-between text-sm mb-1">
                    <span>{fileType.type}</span>
                    <span>{formatSize(fileType.size)}</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-bar-fill bg-secondary" 
                      style={{ 
                        width: `${(fileType.size / scanResults.cleanableSpace) * 100}%` 
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="mt-6 flex space-x-2">
            <button className="btn btn-primary flex-1">
              一键清理
            </button>
            <button className="btn btn-secondary flex-1">
              查看详情
            </button>
          </div>
        </div>
      )}

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">扫描历史</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">扫描时间</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">扫描类型</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">扫描文件数</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">可清理空间</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              <tr>
                <td className="px-4 py-3 text-sm">2026-04-10 14:30</td>
                <td className="px-4 py-3 text-sm">快速扫描</td>
                <td className="px-4 py-3 text-sm">12,500</td>
                <td className="px-4 py-3 text-sm text-primary">25 GB</td>
                <td className="px-4 py-3 text-sm">
                  <button className="text-primary hover:underline">查看</button>
                </td>
              </tr>
              <tr>
                <td className="px-4 py-3 text-sm">2026-04-09 09:15</td>
                <td className="px-4 py-3 text-sm">深度扫描</td>
                <td className="px-4 py-3 text-sm">25,800</td>
                <td className="px-4 py-3 text-sm text-primary">42 GB</td>
                <td className="px-4 py-3 text-sm">
                  <button className="text-primary hover:underline">查看</button>
                </td>
              </tr>
              <tr>
                <td className="px-4 py-3 text-sm">2026-04-08 18:45</td>
                <td className="px-4 py-3 text-sm">智能分析</td>
                <td className="px-4 py-3 text-sm">18,200</td>
                <td className="px-4 py-3 text-sm text-primary">31 GB</td>
                <td className="px-4 py-3 text-sm">
                  <button className="text-primary hover:underline">查看</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ScanPage;