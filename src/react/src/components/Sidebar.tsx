import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar: React.FC = () => {
  const location = useLocation();
  
  const menuItems = [
    { name: '首页', path: '/', icon: '🏠' },
    { name: '扫描', path: '/scan', icon: '🔍' },
    { name: '清理', path: '/clean', icon: '🧹' },
    { name: '空间管理', path: '/space', icon: '📊' },
    { name: '文件恢复', path: '/recovery', icon: '🔄' },
    { name: '系统优化', path: '/optimization', icon: '⚡' },
    { name: '应用管理', path: '/app', icon: '📱' },
    { name: '数据治理', path: '/governance', icon: '📋' },
    { name: '清理历史', path: '/history', icon: '📜' },
    { name: '设置', path: '/settings', icon: '⚙️' },
  ];

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-white shadow-md z-20 overflow-y-auto">
      <div className="p-4 border-b border-gray-200">
        <h1 className="text-xl font-bold text-primary">CleanMaster Pro</h1>
        <p className="text-xs text-gray-500">智能系统清理工具</p>
      </div>
      <div className="p-4">
        <h2 className="text-sm font-semibold text-gray-500 uppercase mb-3">功能导航</h2>
        <ul className="space-y-1">
          {menuItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`flex items-center space-x-3 p-3 rounded-lg transition-all duration-200 ${
                  location.pathname === item.path 
                    ? 'bg-primary text-white font-medium shadow-sm'
                    : 'hover:bg-gray-100 text-gray-700'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.name}</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
        <div className="flex items-center space-x-3 p-3 rounded-lg bg-gray-50">
          <span className="text-xl">ℹ️</span>
          <div>
            <p className="text-sm font-medium">版本 1.0.0</p>
            <p className="text-xs text-gray-500">© 2026 CleanMaster Pro</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;