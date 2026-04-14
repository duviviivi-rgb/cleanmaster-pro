import React, { useState } from 'react';

const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState({
    autoClean: true,
    autoScan: false,
    notification: true,
    theme: 'light',
    language: 'zh-CN',
    scanInterval: 7,
    backupPath: 'D:\\CleanMaster Backup',
    maxFileSize: 100,
    excludedFolders: ['C:\\Windows', 'C:\\Program Files'],
  });

  const handleChange = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-4">设置</h1>
        <p className="text-gray-600 mb-6">配置CleanMaster Pro的各项设置</p>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">基本设置</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span>自动清理</span>
            <label className="switch">
              <input 
                type="checkbox" 
                checked={settings.autoClean}
                onChange={(e) => handleChange('autoClean', e.target.checked)}
              />
              <span className="slider round"></span>
            </label>
          </div>
          <div className="flex items-center justify-between">
            <span>自动扫描</span>
            <label className="switch">
              <input 
                type="checkbox" 
                checked={settings.autoScan}
                onChange={(e) => handleChange('autoScan', e.target.checked)}
              />
              <span className="slider round"></span>
            </label>
          </div>
          <div className="flex items-center justify-between">
            <span>通知提醒</span>
            <label className="switch">
              <input 
                type="checkbox" 
                checked={settings.notification}
                onChange={(e) => handleChange('notification', e.target.checked)}
              />
              <span className="slider round"></span>
            </label>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">界面设置</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">主题</label>
            <select 
              className="w-full p-2 border border-gray-300 rounded-md"
              value={settings.theme}
              onChange={(e) => handleChange('theme', e.target.value)}
            >
              <option value="light">浅色</option>
              <option value="dark">深色</option>
              <option value="system">跟随系统</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">语言</label>
            <select 
              className="w-full p-2 border border-gray-300 rounded-md"
              value={settings.language}
              onChange={(e) => handleChange('language', e.target.value)}
            >
              <option value="zh-CN">简体中文</option>
              <option value="en-US">English</option>
            </select>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">扫描设置</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">自动扫描间隔（天）</label>
            <input 
              type="number" 
              className="w-full p-2 border border-gray-300 rounded-md"
              min="1"
              max="30"
              value={settings.scanInterval}
              onChange={(e) => handleChange('scanInterval', parseInt(e.target.value))}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">最大文件大小（MB）</label>
            <input 
              type="number" 
              className="w-full p-2 border border-gray-300 rounded-md"
              min="1"
              max="1000"
              value={settings.maxFileSize}
              onChange={(e) => handleChange('maxFileSize', parseInt(e.target.value))}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">排除的文件夹</label>
            <div className="space-y-2">
              {settings.excludedFolders.map((folder, index) => (
                <div key={index} className="flex space-x-2">
                  <input 
                    type="text" 
                    className="flex-1 p-2 border border-gray-300 rounded-md"
                    value={folder}
                    onChange={(e) => {
                      const newFolders = [...settings.excludedFolders];
                      newFolders[index] = e.target.value;
                      handleChange('excludedFolders', newFolders);
                    }}
                  />
                  <button 
                    className="btn btn-danger"
                    onClick={() => {
                      const newFolders = settings.excludedFolders.filter((_, i) => i !== index);
                      handleChange('excludedFolders', newFolders);
                    }}
                  >
                    删除
                  </button>
                </div>
              ))}
              <button 
                className="btn btn-secondary w-full"
                onClick={() => {
                  handleChange('excludedFolders', [...settings.excludedFolders, '']);
                }}
              >
                添加文件夹
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">备份设置</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">备份路径</label>
            <input 
              type="text" 
              className="w-full p-2 border border-gray-300 rounded-md"
              value={settings.backupPath}
              onChange={(e) => handleChange('backupPath', e.target.value)}
            />
          </div>
          <button className="btn btn-primary w-full">
            验证路径
          </button>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">关于</h3>
        <div className="space-y-2">
          <p>CleanMaster Pro</p>
          <p className="text-gray-600">版本：1.0.0</p>
          <p className="text-gray-600">版权所有 © 2026 CleanMaster Pro 开发团队</p>
        </div>
      </div>

      <div className="flex space-x-2">
        <button className="btn btn-secondary flex-1">
          恢复默认
        </button>
        <button className="btn btn-primary flex-1">
          保存设置
        </button>
      </div>
    </div>
  );
};

export default SettingsPage;