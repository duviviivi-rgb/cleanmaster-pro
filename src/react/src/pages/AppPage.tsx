import React, { useState } from 'react';

const AppPage: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [applications, _setApplications] = useState([
    { id: '1', name: 'Google Chrome', version: '123.0.6312.105', publisher: 'Google LLC', installDate: '2026-03-15', size: 1500000000, status: 'healthy', recommendation: 'keep' },
    { id: '2', name: 'Discord', version: '0.0.306', publisher: 'Discord Inc.', installDate: '2026-02-20', size: 800000000, status: 'healthy', recommendation: 'keep' },
    { id: '3', name: 'Steam', version: '1669807911', publisher: 'Valve Corporation', installDate: '2026-01-10', size: 2000000000, status: 'healthy', recommendation: 'keep' },
    { id: '4', name: 'Microsoft Office', version: '2021', publisher: 'Microsoft Corporation', installDate: '2025-12-01', size: 3000000000, status: 'healthy', recommendation: 'keep' },
    { id: '5', name: 'Old App', version: '1.0.0', publisher: 'Unknown', installDate: '2025-06-15', size: 500000000, status: 'dormant', recommendation: 'remove' },
    { id: '6', name: 'Broken App', version: '2.0.0', publisher: 'Unknown', installDate: '2025-08-20', size: 300000000, status: 'broken', recommendation: 'remove' },
  ]);
  const [selectedApps, setSelectedApps] = useState<string[]>([]);
  const [isUninstalling, setIsUninstalling] = useState(false);
  const [uninstallProgress, setUninstallProgress] = useState(0);

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

  const toggleAppSelection = (appId: string) => {
    setSelectedApps(prev => {
      if (prev.includes(appId)) {
        return prev.filter(id => id !== appId);
      } else {
        return [...prev, appId];
      }
    });
  };

  const startUninstall = () => {
    if (selectedApps.length === 0) return;
    
    setIsUninstalling(true);
    setUninstallProgress(0);
    
    // 模拟卸载过程
    const interval = setInterval(() => {
      setUninstallProgress(prev => {
        const newProgress = prev + 10;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsUninstalling(false);
          // 模拟卸载完成
          alert('应用卸载成功！');
          return 100;
        }
        return newProgress;
      });
    }, 300);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">应用管理</h1>
        <p className="text-gray-600 mb-6">扫描和管理应用程序，卸载不需要的应用</p>
      </div>

      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">扫描应用程序</h3>
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
              正在扫描... 已发现 {Math.floor(progress * 0.06)} 个应用程序
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">应用程序列表</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">
                  <input type="checkbox" className="mr-2" />
                </th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">名称</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">版本</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">发布者</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">安装日期</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">大小</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">状态</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">建议</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {applications.map((app) => (
                <tr key={app.id}>
                  <td className="px-4 py-3">
                    <input 
                      type="checkbox" 
                      className="mr-2" 
                      checked={selectedApps.includes(app.id)}
                      onChange={() => toggleAppSelection(app.id)}
                    />
                  </td>
                  <td className="px-4 py-3 text-sm font-medium">{app.name}</td>
                  <td className="px-4 py-3 text-sm">{app.version}</td>
                  <td className="px-4 py-3 text-sm">{app.publisher}</td>
                  <td className="px-4 py-3 text-sm">{app.installDate}</td>
                  <td className="px-4 py-3 text-sm">{formatSize(app.size)}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      app.status === 'healthy' ? 'bg-green-100 text-green-800' :
                      app.status === 'dormant' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {app.status === 'healthy' ? '健康' :
                       app.status === 'dormant' ? '沉睡' :
                       '损坏'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      app.recommendation === 'keep' ? 'bg-green-100 text-green-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {app.recommendation === 'keep' ? '保留' : '卸载'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm">
                    <button className="text-primary hover:underline mr-2">详情</button>
                    <button className="text-primary hover:underline">卸载</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-4 flex justify-between items-center">
          <div className="text-sm">
            已选择 {selectedApps.length} 个应用
          </div>
          <button 
            className="btn btn-danger" 
            onClick={startUninstall}
            disabled={selectedApps.length === 0 || isUninstalling}
          >
            {isUninstalling ? '卸载中...' : '卸载选中应用'}
          </button>
        </div>
        {isUninstalling && (
          <div className="mt-4 space-y-2">
            <div className="progress-bar">
              <div 
                className="progress-bar-fill bg-danger" 
                style={{ width: `${uninstallProgress}%` }}
              ></div>
            </div>
            <div className="flex justify-between text-sm">
              <span>卸载进度</span>
              <span>{uninstallProgress}%</span>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">应用清理建议</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">总应用数</p>
            <p className="text-2xl font-bold">6</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">建议卸载</p>
            <p className="text-2xl font-bold text-danger">2</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">预计节省空间</p>
            <p className="text-2xl font-bold text-primary">800 MB</p>
          </div>
        </div>
        <button className="btn btn-primary w-full">
          一键卸载建议应用
        </button>
      </div>
    </div>
  );
};

export default AppPage;