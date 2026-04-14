import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: '首页', icon: '🏠' },
    { path: '/scan', label: '扫描', icon: '🔍' },
    { path: '/clean', label: '清理', icon: '🧹' },
    { path: '/space', label: '空间管理', icon: '📊' },
    { path: '/recovery', label: '文件恢复', icon: '🔄' },
    { path: '/optimization', label: '系统优化', icon: '⚡' },
    { path: '/apps', label: '应用管理', icon: '📱' },
    { path: '/governance', label: '数据治理', icon: '📋' },
    { path: '/history', label: '清理历史', icon: '📜' },
    { path: '/settings', label: '设置', icon: '⚙️' },
  ];

  return (
    <div className="w-64 bg-white shadow-md">
      <div className="p-4 border-b">
        <h1 className="text-xl font-bold text-blue-600">CleanMaster Pro</h1>
      </div>
      <nav className="p-4">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${location.pathname === item.path ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'}`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default Navbar;