import React, { useState } from 'react';

const HistoryPage: React.FC = () => {
  const [selectedPeriod, setSelectedPeriod] = useState<'today' | 'week' | 'month' | 'all'>('week');
  
  // 模拟历史数据
  const history = [
    {
      id: 1,
      type: '标准清理',
      date: '2024-04-10T14:30:00',
      spaceSaved: 2500000000,
      filesDeleted: 150,
      duration: '1m 30s'
    },
    {
      id: 2,
      type: '快速清理',
      date: '2024-04-09T10:15:00',
      spaceSaved: 1200000000,
      filesDeleted: 80,
      duration: '30s'
    },
    {
      id: 3,
      type: '深度清理',
      date: '2024-04-07T20:45:00',
      spaceSaved: 5000000000,
      filesDeleted: 300,
      duration: '3m 15s'
    },
    {
      id: 4,
      type: '标准清理',
      date: '2024-04-05T16:20:00',
      spaceSaved: 2000000000,
      filesDeleted: 120,
      duration: '1m 15s'
    },
    {
      id: 5,
      type: '快速清理',
      date: '2024-04-03T09:30:00',
      spaceSaved: 800000000,
      filesDeleted: 50,
      duration: '25s'
    }
  ];

  const getFilteredHistory = () => {
    const now = new Date();
    return history.filter(item => {
      const itemDate = new Date(item.date);
      const diffTime = now.getTime() - itemDate.getTime();
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (selectedPeriod === 'today') {
        return diffDays <= 1;
      } else if (selectedPeriod === 'week') {
        return diffDays <= 7;
      } else if (selectedPeriod === 'month') {
        return diffDays <= 30;
      }
      return true;
    });
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
      <h1 className="text-2xl font-bold mb-6">清理历史</h1>
      
      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-6">
          <div className="flex border-b">
            <button 
              onClick={() => setSelectedPeriod('today')}
              className={`px-4 py-2 ${selectedPeriod === 'today' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            >
              今天
            </button>
            <button 
              onClick={() => setSelectedPeriod('week')}
              className={`px-4 py-2 ${selectedPeriod === 'week' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            >
              本周
            </button>
            <button 
              onClick={() => setSelectedPeriod('month')}
              className={`px-4 py-2 ${selectedPeriod === 'month' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            >
              本月
            </button>
            <button 
              onClick={() => setSelectedPeriod('all')}
              className={`px-4 py-2 ${selectedPeriod === 'all' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            >
              全部
            </button>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  清理类型
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  日期时间
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  节省空间
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  删除文件数
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  耗时
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {getFilteredHistory().map((item) => (
                <tr key={item.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {item.type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(item.date)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatBytes(item.spaceSaved)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.filesDeleted}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.duration}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="mt-6">
          <button className="text-red-600 hover:text-red-900">
            清空历史记录
          </button>
        </div>
      </div>
    </div>
  );
};

export default HistoryPage;