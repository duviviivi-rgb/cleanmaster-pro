import React, { useState } from 'react';

const ScanPage: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [scanType, setScanType] = useState<'quick' | 'deep' | 'smart'>('quick');
  const [scanResults, setScanResults] = useState<any>(null);

  const startScan = () => {
    setIsScanning(true);
    setProgress(0);
    
    // 模拟扫描过程
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsScanning(false);
          // 模拟扫描结果
          setScanResults({
            totalSpace: 135000000000,
            usedSpace: 100000000000,
            cleanableSpace: 2500000000,
            fileTypes: [
              { type: '临时文件', size: 1000000000, percentage: 40 },
              { type: '浏览器缓存', size: 750000000, percentage: 30 },
              { type: '系统日志', size: 500000000, percentage: 20 },
              { type: '其他', size: 250000000, percentage: 10 }
            ]
          });
          return 100;
        }
        return prev + 5;
      });
    }, 200);
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
      <h1 className="text-2xl font-bold mb-6">扫描</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">选择扫描类型</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <button 
            onClick={() => setScanType('quick')}
            className={`p-4 rounded-lg border ${scanType === 'quick' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">快速扫描</h3>
            <p className="text-sm text-gray-600">扫描临时文件和缓存</p>
          </button>
          <button 
            onClick={() => setScanType('deep')}
            className={`p-4 rounded-lg border ${scanType === 'deep' ? 'border-purple-500 bg-purple-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">深度扫描</h3>
            <p className="text-sm text-gray-600">详细分析磁盘内容</p>
          </button>
          <button 
            onClick={() => setScanType('smart')}
            className={`p-4 rounded-lg border ${scanType === 'smart' ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">智能分析</h3>
            <p className="text-sm text-gray-600">基于使用习惯分析</p>
          </button>
        </div>
        
        <button 
          onClick={startScan}
          disabled={isScanning}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
        >
          {isScanning ? '扫描中...' : '开始扫描'}
        </button>
      </div>

      {isScanning && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4">扫描进度</h2>
          <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
            <div 
              className="bg-blue-600 h-4 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="flex justify-between text-sm">
            <span>正在扫描 {scanType === 'quick' ? '临时文件和缓存' : scanType === 'deep' ? '磁盘内容' : '使用习惯'}</span>
            <span>{progress}%</span>
          </div>
        </div>
      )}

      {scanResults && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">扫描结果</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <div className="text-gray-500 text-sm">总空间</div>
              <div className="font-medium">{formatBytes(scanResults.totalSpace)}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">已用空间</div>
              <div className="font-medium">{formatBytes(scanResults.usedSpace)}</div>
            </div>
            <div>
              <div className="text-gray-500 text-sm">可清理空间</div>
              <div className="font-medium text-green-600">{formatBytes(scanResults.cleanableSpace)}</div>
            </div>
          </div>
          
          <h3 className="font-medium mb-3">文件类型分布</h3>
          <div className="space-y-3">
            {scanResults.fileTypes.map((type: any, index: number) => (
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
          
          <div className="mt-6">
            <button className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors">
              执行清理
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScanPage;