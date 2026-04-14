import React, { useState } from 'react';

const AppPage: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState<'all' | 'uninstall' | 'large'>('all');
  
  // 模拟应用数据
  const apps = [
    {
      id: 1,
      name: 'Google Chrome',
      version: '120.0.6099.224',
      size: 300000000,
      installDate: '2024-01-15',
      canUninstall: true
    },
    {
      id: 2,
      name: 'Microsoft Office',
      version: '2021',
      size: 2000000000,
      installDate: '2023-11-20',
      canUninstall: true
    },
    {
      id: 3,
      name: 'Adobe Photoshop',
      version: '24.7.0',
      size: 1500000000,
      installDate: '2024-02-10',
      canUninstall: true
    },
    {
      id: 4,
      name: 'Windows Calculator',
      version: '10.2103.8.0',
      size: 50000000,
      installDate: '2023-10-05',
      canUninstall: false
    },
    {
      id: 5,
      name: 'Visual Studio Code',
      version: '1.85.0',
      size: 350000000,
      installDate: '2024-01-01',
      canUninstall: true
    }
  ];

  const getFilteredApps = () => {
    if (selectedTab === 'all') {
      return apps;
    } else if (selectedTab === 'uninstall') {
      return apps.filter(app => app.canUninstall);
    } else if (selectedTab === 'large') {
      return apps.filter(app => app.size > 1000000000);
    }
    return apps;
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
      <h1 className="text-2xl font-bold mb-6">应用管理</h1>
      
      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-6">
          <div className="flex border-b">
            <button 
              onClick={() => setSelectedTab('all')}
              className={`px-4 py-2 ${selectedTab === 'all' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            >
              所有应用
            </button>
            <button 
              onClick={() => setSelectedTab('uninstall')}
              className={`px-4 py-2 ${selectedTab === 'uninstall' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            >
              可卸载
            </button>
            <button 
              onClick={() => setSelectedTab('large')}
              className={`px-4 py-2 ${selectedTab === 'large' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            >
              大型应用
            </button>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  应用名称
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  版本
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  大小
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  安装日期
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {getFilteredApps().map((app) => (
                <tr key={app.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {app.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {app.version}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatBytes(app.size)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {app.installDate}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button 
                      disabled={!app.canUninstall}
                      className={`text-red-600 hover:text-red-900 ${!app.canUninstall ? 'text-gray-400 cursor-not-allowed' : ''}`}
                    >
                      卸载
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AppPage;