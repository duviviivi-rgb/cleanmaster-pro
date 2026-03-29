// 测试API服务
import * as api from './src/react/services/api';

async function testApi() {
  console.log('开始测试API服务...');
  
  try {
    // 测试磁盘信息接口
    console.log('测试磁盘信息接口...');
    const disks = await api.diskApi.getDisks();
    console.log('磁盘信息:', disks);
    
    // 测试设置接口
    console.log('测试设置接口...');
    const settings = await api.settingsApi.getSettings();
    console.log('用户设置:', settings);
    
    // 测试快速扫描接口
    console.log('测试快速扫描接口...');
    const quickScan = await api.scanApi.quickScan();
    console.log('快速扫描结果:', quickScan);
    
    // 测试深度扫描接口
    console.log('测试深度扫描接口...');
    const deepScan = await api.scanApi.deepScan();
    console.log('深度扫描结果:', deepScan);
    
    // 测试智能分析接口
    console.log('测试智能分析接口...');
    const analysis = await api.scanApi.intelligentAnalysis();
    console.log('智能分析结果:', analysis);
    
    // 测试空间使用情况接口
    console.log('测试空间使用情况接口...');
    const spaceUsage = await api.spaceApi.getSpaceUsage();
    console.log('空间使用情况:', spaceUsage);
    
    // 测试可恢复文件接口
    console.log('测试可恢复文件接口...');
    const recoverableFiles = await api.recoveryApi.scanRecoverableFiles();
    console.log('可恢复文件:', recoverableFiles);
    
    // 测试启动项接口
    console.log('测试启动项接口...');
    const startupItems = await api.optimizationApi.getStartupItems();
    console.log('启动项:', startupItems);
    
    // 测试清理历史接口
    console.log('测试清理历史接口...');
    const cleanHistory = await api.historyApi.getCleanHistory();
    console.log('清理历史:', cleanHistory);
    
    console.log('API服务测试成功!');
  } catch (error) {
    console.error('API服务测试失败:', error);
  }
}

testApi();
