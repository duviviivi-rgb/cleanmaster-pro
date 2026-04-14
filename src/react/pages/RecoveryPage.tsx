import React, { useState } from 'react';

const RecoveryPage: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [recoveryType, setRecoveryType] = useState<'recent' | 'deep' | 'specific'>('recent');
  const [recoveryResults, setRecoveryResults] = useState<any[]>([]);

  const startScan = () => {
    setIsScanning(true);
    setProgress(0);
    
    // 模拟扫描过程
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsScanning(false);
          // 模拟恢复结果
          setRecoveryResults([
            {
              id: 1,
              name: 'document.docx',
              path: 'C:\\Users\\User\\Documents',
              size: 1048576,
              deletedDate: '2024-04-01T10:30:00',
              recoverable: true
            },
            {
              id: 2,
              name: 'image.jpg',
              path: 'C:\\Users\\User\\Pictures',
              size: 2097152,
              deletedDate: '2024-04-02T15:45:00',
              recoverable: true
            },
            {
              id: 3,
              name: 'video.mp4',
              path: 'C:\\Users\\User\\Videos',
              size: 10485760,
              deletedDate: '2024-04-03T09:15:00',
              recoverable: false
            },
            {
              id: 4,
              name: 'spreadsheet.xlsx',
              path: 'C:\\Users\\User\\Documents',
              size: 1572864,
              deletedDate: '2024-04-04T14:20:00',
              recoverable: true
            }
          ]);
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

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">文件恢复</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">选择恢复类型</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <button 
            onClick={() => setRecoveryType('recent')}
            className={`p-4 rounded-lg border ${recoveryType === 'recent' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">最近删除</h3>
            <p className="text-sm text-gray-600">恢复最近删除的文件</p>
          </button>
          <button 
            onClick={() => setRecoveryType('deep')}
            className={`p-4 rounded-lg border ${recoveryType === 'deep' ? 'border-purple-500 bg-purple-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">深度扫描</h3>
            <p className="text-sm text-gray-600">全面扫描可恢复文件</p>
          </button>
          <button 
            onClick={() => setRecoveryType('specific')}
            className={`p-4 rounded-lg border ${recoveryType === 'specific' ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}
          >
            <h3 className="font-medium mb-1">指定位置</h3>
            <p className="text-sm text-gray-600">扫描特定目录</p>
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
            <span>正在扫描可恢复文件</span>
            <span>{progress}%</span>
          </div>
        </div>
      )}

      {recoveryResults.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">可恢复文件</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    文件名
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    路径
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    大小
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    删除时间
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    状态
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recoveryResults.map((file) => (
                  <tr key={file.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {file.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {file.path}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatBytes(file.size)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(file.deletedDate)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${file.recoverable ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {file.recoverable ? '可恢复' : '不可恢复'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button 
                        disabled={!file.recoverable}
                        className={`text-blue-600 hover:text-blue-900 ${!file.recoverable ? 'text-gray-400 cursor-not-allowed' : ''}`}
                      >
                        恢复
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecoveryPage;