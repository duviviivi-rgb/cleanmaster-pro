import React, { useState, useEffect } from 'react';
import apiService from '../services/api';

const HomePage: React.FC = () => {
  const [disks, setDisks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 获取磁盘信息
    const fetchDisks = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiService.getDisks();
        if (response && response.data) {
          setDisks(response.data);
        } else {
          setError('获取磁盘信息失败');
        }
      } catch (err) {
        setError('网络错误，请稍后重试');
        console.error('获取磁盘信息错误:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDisks();
  }, []);

  const formatSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getProgressColor = (percentage: number): string => {
    if (percentage < 60) return 'bg-success';
    if (percentage < 80) return 'bg-warning';
    return 'bg-danger';
  };

  const handleScan = async (disk: string) => {
    try {
      await apiService.startScan(disk, 'quick');
      alert('扫描已开始');
    } catch (err) {
      alert('扫描失败，请稍后重试');
      console.error('扫描错误:', err);
    }
  };

  const handleClean = async (disk: string) => {
    try {
      await apiService.startClean(disk, []);
      alert('清理已开始');
    } catch (err) {
      alert('清理失败，请稍后重试');
      console.error('清理错误:', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">磁盘概览</h1>
        <button 
          className="btn btn-primary"
          onClick={() => handleScan('C:')}
        >
          立即扫描
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
        </div>
      ) : error ? (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded" role="alert">
          <strong className="font-bold">错误: </strong>
          <span className="block sm:inline">{error}</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {disks.map((disk) => {
            const usedPercentage = (disk.usedSpace / disk.totalSpace) * 100;
            return (
              <div key={disk.letter} className="card">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold">{disk.letter} {disk.name}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    disk.healthStatus === 'healthy' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {disk.healthStatus === 'healthy' ? '健康' : '警告'}
                  </span>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>已用空间</span>
                    <span>{formatSize(disk.usedSpace)} / {formatSize(disk.totalSpace)}</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className={`progress-bar-fill ${getProgressColor(usedPercentage)}`} 
                      style={{ width: `${usedPercentage}%` }}
                    ></div>
                  </div>
                  <div className="flex justify-end text-sm font-medium">
                    {usedPercentage.toFixed(1)}%
                  </div>
                </div>
                <div className="mt-4 flex space-x-2">
                  <button 
                    className="btn btn-secondary flex-1"
                    onClick={() => handleScan(disk.letter)}
                  >
                    扫描
                  </button>
                  <button 
                    className="btn btn-primary flex-1"
                    onClick={() => handleClean(disk.letter)}
                  >
                    清理
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">快速操作</h3>
          <div className="grid grid-cols-2 gap-4">
            <button 
              className="btn btn-primary"
              onClick={() => handleScan('C:')}
            >
              快速扫描
            </button>
            <button 
              className="btn btn-secondary"
              onClick={() => handleScan('C:')}
            >
              深度扫描
            </button>
            <button className="btn btn-success">
              空间分析
            </button>
            <button className="btn btn-warning">
              系统优化
            </button>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">系统状态</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>CPU使用率</span>
                <span>35%</span>
              </div>
              <div className="progress-bar">
                <div className="progress-bar-fill bg-primary" style={{ width: '35%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>内存使用率</span>
                <span>48%</span>
              </div>
              <div className="progress-bar">
                <div className="progress-bar-fill bg-primary" style={{ width: '48%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>上次清理</span>
                <span>2026-04-10 14:30</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;