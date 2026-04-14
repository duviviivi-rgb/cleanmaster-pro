import React, { useState } from 'react';

const HistoryPage: React.FC = () => {
  const [cleanHistory, setCleanHistory] = useState([
    { id: '1', timestamp: '2026-04-10 14:30', disk: 'C:', cleanType: '快速扫描', spaceSaved: 25000000000, filesDeleted: 3200, duration: 60 },
    { id: '2', timestamp: '2026-04-09 09:15', disk: 'C:', cleanType: '深度扫描', spaceSaved: 42000000000, filesDeleted: 5800, duration: 120 },
    { id: '3', timestamp: '2026-04-08 18:45', disk: 'D:', cleanType: '智能分析', spaceSaved: 31000000000, filesDeleted: 4500, duration: 90 },
    { id: '4', timestamp: '2026-04-07 12:00', disk: 'C:', cleanType: '快速扫描', spaceSaved: 18000000000, filesDeleted: 2500, duration: 45 },
    { id: '5', timestamp: '2026-04-06 10:30', disk: 'E:', cleanType: '深度扫描', spaceSaved: 56000000000, filesDeleted: 7200, duration: 150 },
  ]);
  const [analysis, setAnalysis] = useState({
    totalSpaceSaved: 172000000000,
    averageCleanTime: 93,
    mostCleanedType: '深度扫描',
    totalCleanings: 5,
    mostActiveDay: 'Monday',
  });

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
        <h1 className="text-2xl font-bold mb-4">清理历史</h1>
        <p className="text-gray-600 mb-6">查看清理历史记录，分析清理效果</p>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">清理效果分析</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">总节省空间</p>
            <p className="text-2xl font-bold text-primary">{formatSize(analysis.totalSpaceSaved)}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">平均清理时间</p>
            <p className="text-2xl font-bold">{analysis.averageCleanTime} 秒</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">最常见清理类型</p>
            <p className="text-2xl font-bold">{analysis.mostCleanedType}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">总清理次数</p>
            <p className="text-2xl font-bold">{analysis.totalCleanings} 次</p>
          </div>
        </div>
        <div className="flex space-x-2">
          <button className="btn btn-secondary flex-1">
            导出分析
          </button>
          <button className="btn btn-primary flex-1">
            清理历史
          </button>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">清理历史记录</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">时间</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">磁盘</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">清理类型</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">节省空间</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">删除文件数</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">耗时</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-600">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {cleanHistory.map((record) => (
                <tr key={record.id}>
                  <td className="px-4 py-3 text-sm">{record.timestamp}</td>
                  <td className="px-4 py-3 text-sm">{record.disk}</td>
                  <td className="px-4 py-3 text-sm">{record.cleanType}</td>
                  <td className="px-4 py-3 text-sm text-primary">{formatSize(record.spaceSaved)}</td>
                  <td className="px-4 py-3 text-sm">{record.filesDeleted.toLocaleString()}</td>
                  <td className="px-4 py-3 text-sm">{record.duration} 秒</td>
                  <td className="px-4 py-3 text-sm">
                    <button className="text-primary hover:underline">查看</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">清理趋势</h3>
        <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <p className="text-gray-500">清理趋势图表</p>
        </div>
      </div>
    </div>
  );
};

export default HistoryPage;