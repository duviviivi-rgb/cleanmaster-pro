import React, { useState } from 'react';

const RecoveryPage: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [recoverableFiles, setRecoverableFiles] = useState([
    { id: '1', name: 'document.docx', path: 'C:\\Documents\\document.docx', size: 2000000, deletedDate: '2026-04-10 14:30', recoveryChance: 'high' },
    { id: '2', name: 'photo.jpg', path: 'C:\\Pictures\\photo.jpg', size: 5000000, deletedDate: '2026-04-09 09:15', recoveryChance: 'medium' },
    { id: '3', name: 'video.mp4', path: 'C:\\Videos\\video.mp4', size: 50000000, deletedDate: '2026-04-08 18:45', recoveryChance: 'low' },
    { id: '4', name: 'spreadsheet.xlsx', path: 'C:\\Documents\\spreadsheet.xlsx', size: 1500000, deletedDate: '2026-04-07 12:00', recoveryChance: 'high' },
    { id: '5', name: 'presentation.pptx', path: 'C:\\Documents\\presentation.pptx', size: 8000000, deletedDate: '2026-04-06 10:30', recoveryChance: 'medium' },
  ]);
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const [isRecovering, setIsRecovering] = useState(false);
  const [recoveryProgress, setRecoveryProgress] = useState(0);

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

  const toggleFileSelection = (fileId: string) => {
    setSelectedFiles(prev => {
      if (prev.includes(fileId)) {
        return prev.filter(id => id !== fileId);
      } else {
        return [...prev, fileId];
      }
    });
  };

  const startRecovery = () => {
    if (selectedFiles.length === 0) return;
    
    setIsRecovering(true);
    setRecoveryProgress(0);
    
    // 模拟恢复过程
    const interval = setInterval(() => {
      setRecoveryProgress(prev => {
        const newProgress = prev + 10;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsRecovering(false);
          // 模拟恢复完成
          alert('文件恢复成功！');
          return 100;
        }
        return newProgress;
      });
    }, 300);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">文件恢复</h1>
        <p className="text-gray-600 mb-6">扫描可恢复文件，恢复误删除的文件</p>
      </div>

      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">扫描可恢复文件</h3>
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
              正在扫描... 已发现 {Math.floor(progress * 0.05)} 个可恢复文件
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">可恢复文件</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">
                  <input type="checkbox" className="mr-2" />
                </th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">文件名</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">路径</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">大小</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">删除时间</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">恢复成功率</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {recoverableFiles.map((file) => (
                <tr key={file.id}>
                  <td className="px-4 py-3">
                    <input 
                      type="checkbox" 
                      className="mr-2" 
                      checked={selectedFiles.includes(file.id)}
                      onChange={() => toggleFileSelection(file.id)}
                    />
                  </td>
                  <td className="px-4 py-3 text-sm font-medium">{file.name}</td>
                  <td className="px-4 py-3 text-sm text-gray-600 truncate w-48">{file.path}</td>
                  <td className="px-4 py-3 text-sm">{formatSize(file.size)}</td>
                  <td className="px-4 py-3 text-sm">{file.deletedDate}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      file.recoveryChance === 'high' ? 'bg-green-100 text-green-800' :
                      file.recoveryChance === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {file.recoveryChance === 'high' ? '高' :
                       file.recoveryChance === 'medium' ? '中' :
                       '低'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm">
                    <button className="text-primary hover:underline mr-2">预览</button>
                    <button className="text-primary hover:underline">恢复</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-4 flex justify-between items-center">
          <div className="text-sm">
            已选择 {selectedFiles.length} 个文件
          </div>
          <button 
            className="btn btn-primary" 
            onClick={startRecovery}
            disabled={selectedFiles.length === 0 || isRecovering}
          >
            {isRecovering ? '恢复中...' : '恢复选中文件'}
          </button>
        </div>
        {isRecovering && (
          <div className="mt-4 space-y-2">
            <div className="progress-bar">
              <div 
                className="progress-bar-fill bg-success" 
                style={{ width: `${recoveryProgress}%` }}
              ></div>
            </div>
            <div className="flex justify-between text-sm">
              <span>恢复进度</span>
              <span>{recoveryProgress}%</span>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">恢复历史</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">恢复时间</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">恢复文件数</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">恢复路径</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">状态</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              <tr>
                <td className="px-4 py-3 text-sm">2026-04-10 14:30</td>
                <td className="px-4 py-3 text-sm">3</td>
                <td className="px-4 py-3 text-sm">C:\\Recovered</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">成功</span>
                </td>
              </tr>
              <tr>
                <td className="px-4 py-3 text-sm">2026-04-09 09:15</td>
                <td className="px-4 py-3 text-sm">2</td>
                <td className="px-4 py-3 text-sm">C:\\Recovered</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">成功</span>
                </td>
              </tr>
              <tr>
                <td className="px-4 py-3 text-sm">2026-04-08 18:45</td>
                <td className="px-4 py-3 text-sm">1</td>
                <td className="px-4 py-3 text-sm">C:\\Recovered</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">部分成功</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default RecoveryPage;