import { useState, useEffect, memo, useCallback } from 'react'
import { AppProvider, useApp } from './context/AppContext'

// 安抚色系配置
const colors = {
  primary: '#5B8C85',      // 莫兰迪绿 - 主色
  primaryLight: '#7BA598', // 浅绿
  primaryDark: '#4A736D',  // 深绿
  secondary: '#E8D5C4',    // 米色
  accent: '#D4A5A5',       // 灰粉
  success: '#8FBC8F',      // 柔和绿
  warning: '#DEB887',      // 柔和棕
  danger: '#CD5C5C',       // 柔和红
  bgLight: '#F5F5F0',      // 米白背景
  bgDark: '#2D3436',       // 深灰背景
  textLight: '#5D5D5D',    // 浅灰文字
  textDark: '#E8E8E8',     // 浅白文字
}

// 磁盘信息组件
const DiskInfoItem = memo(({ disk }: { disk: any }) => {
  const percentage = disk.percentage
  let barColor = colors.success
  if (percentage > 70) barColor = colors.warning
  if (percentage > 85) barColor = colors.danger

  return (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm font-medium" style={{ color: colors.textLight }}>
          {disk.letter} {disk.name}
        </span>
        <span className="text-xs" style={{ color: colors.textLight }}>
          {percentage}%
        </span>
      </div>
      <div className="w-full rounded-full h-2" style={{ backgroundColor: '#E0E0E0' }}>
        <div 
          className="h-2 rounded-full transition-all duration-500"
          style={{ width: `${percentage}%`, backgroundColor: barColor }}
        />
      </div>
      <div className="flex justify-between mt-1 text-xs" style={{ color: colors.textLight }}>
        <span>已用 {(disk.usedSpace / 1e9).toFixed(1)} GB</span>
        <span>可用 {(disk.freeSpace / 1e9).toFixed(1)} GB</span>
      </div>
    </div>
  )
})

// 主应用组件
function AppContent() {
  const [activeTab, setActiveTab] = useState('home')
  const [isScanning, setIsScanning] = useState(false)
  const [scanProgress, setScanProgress] = useState(0)
  const [scanResult, setScanResult] = useState<any>(null)
  const [showResult, setShowResult] = useState(false)
  const { state, toggleTheme, changeLanguage, loadDisks } = useApp()

  // 应用主题
  useEffect(() => {
    if (state.settings.theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [state.settings.theme])

  // 一键扫描并清理
  const handleOneClickClean = useCallback(async () => {
    setIsScanning(true)
    setScanProgress(0)
    setShowResult(false)

    // 模拟扫描进度
    const interval = setInterval(() => {
      setScanProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 5
      })
    }, 100)

    // 模拟扫描完成
    setTimeout(() => {
      setIsScanning(false)
      setScanResult({
        cleanableSpace: 2.5 * 1024 * 1024 * 1024, // 2.5GB
        fileCount: 156,
        categories: [
          { name: '临时文件', size: 1.2 * 1024 * 1024 * 1024, count: 89 },
          { name: '浏览器缓存', size: 0.8 * 1024 * 1024 * 1024, count: 45 },
          { name: '系统日志', size: 0.3 * 1024 * 1024 * 1024, count: 15 },
          { name: '回收站', size: 0.2 * 1024 * 1024 * 1024, count: 7 },
        ]
      })
      setShowResult(true)
    }, 2500)
  }, [])

  // 确认清理
  const handleConfirmClean = useCallback(() => {
    // 模拟清理
    setShowResult(false)
    setTimeout(() => {
      alert('清理完成！已释放 2.5GB 空间')
      loadDisks()
    }, 500)
  }, [loadDisks])

  // 格式化大小
  const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const isDark = state.settings.theme === 'dark'
  const bgColor = isDark ? colors.bgDark : colors.bgLight
  const textColor = isDark ? colors.textDark : colors.textLight

  return (
    <div className="min-h-screen transition-colors duration-300" style={{ backgroundColor: bgColor, color: textColor }}>
      {/* 顶部导航 - 极简风格 */}
      <nav className="px-4 py-3 shadow-sm" style={{ backgroundColor: isDark ? '#1E2527' : '#FFFFFF' }}>
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold"
              style={{ backgroundColor: colors.primary }}
            >
              C
            </div>
            <span className="font-semibold text-lg" style={{ color: colors.primary }}>CleanMaster</span>
          </div>
          <div className="flex items-center gap-2">
            <button 
              onClick={() => setActiveTab('home')}
              className={`px-3 py-1.5 rounded-full text-sm transition-all ${activeTab === 'home' ? 'text-white' : 'hover:opacity-80'}`}
              style={{ backgroundColor: activeTab === 'home' ? colors.primary : 'transparent' }}
            >
              首页
            </button>
            <button 
              onClick={() => setActiveTab('settings')}
              className={`px-3 py-1.5 rounded-full text-sm transition-all ${activeTab === 'settings' ? 'text-white' : 'hover:opacity-80'}`}
              style={{ backgroundColor: activeTab === 'settings' ? colors.primary : 'transparent' }}
            >
              设置
            </button>
          </div>
        </div>
      </nav>

      {/* 主要内容 */}
      <main className="max-w-4xl mx-auto p-4">
        {activeTab === 'home' && (
          <div className="space-y-6">
            {/* 一键清理卡片 */}
            <div 
              className="rounded-2xl p-6 text-center shadow-sm"
              style={{ backgroundColor: isDark ? '#1E2527' : '#FFFFFF' }}
            >
              <h2 className="text-xl font-medium mb-2" style={{ color: colors.primary }}>磁盘清理</h2>
              <p className="text-sm mb-6 opacity-70">一键扫描并清理系统垃圾文件</p>

              {/* 磁盘使用概览 */}
              <div className="flex justify-center gap-4 mb-6">
                {state.disks.slice(0, 2).map(disk => (
                  <div key={disk.letter} className="text-center">
                    <div 
                      className="text-2xl font-bold"
                      style={{ color: disk.percentage > 85 ? colors.danger : colors.primary }}
                    >
                      {disk.percentage}%
                    </div>
                    <div className="text-xs opacity-60">{disk.letter}</div>
                  </div>
                ))}
              </div>

              {/* 一键按钮 */}
              {!isScanning && !showResult && (
                <button
                  onClick={handleOneClickClean}
                  className="w-full sm:w-auto px-12 py-4 rounded-full text-white font-medium text-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
                  style={{ backgroundColor: colors.primary }}
                >
                  一键扫描清理
                </button>
              )}

              {/* 扫描进度 */}
              {isScanning && (
                <div className="max-w-md mx-auto">
                  <div className="flex justify-between text-sm mb-2 opacity-70">
                    <span>正在扫描...</span>
                    <span>{scanProgress}%</span>
                  </div>
                  <div className="w-full rounded-full h-3 overflow-hidden" style={{ backgroundColor: '#E0E0E0' }}>
                    <div 
                      className="h-full rounded-full transition-all duration-100"
                      style={{ width: `${scanProgress}%`, backgroundColor: colors.primary }}
                    />
                  </div>
                </div>
              )}

              {/* 扫描结果 */}
              {showResult && scanResult && (
                <div className="max-w-md mx-auto text-left">
                  <div 
                    className="rounded-xl p-4 mb-4"
                    style={{ backgroundColor: colors.secondary + '30' }}
                  >
                    <div className="flex justify-between items-center mb-3">
                      <span className="font-medium">可清理空间</span>
                      <span className="text-2xl font-bold" style={{ color: colors.primary }}>
                        {formatSize(scanResult.cleanableSpace)}
                      </span>
                    </div>
                    <div className="text-sm opacity-70 mb-3">共 {scanResult.fileCount} 个文件</div>
                    <div className="space-y-2">
                      {scanResult.categories.map((cat: any) => (
                        <div key={cat.name} className="flex justify-between text-sm">
                          <span>{cat.name}</span>
                          <span>{formatSize(cat.size)} ({cat.count}个)</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <button
                      onClick={handleConfirmClean}
                      className="flex-1 py-3 rounded-full text-white font-medium shadow-md hover:shadow-lg transition-all"
                      style={{ backgroundColor: colors.success }}
                    >
                      立即清理
                    </button>
                    <button
                      onClick={() => setShowResult(false)}
                      className="flex-1 py-3 rounded-full font-medium border transition-all hover:opacity-80"
                      style={{ borderColor: colors.textLight, color: colors.textLight }}
                    >
                      取消
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* 磁盘详情 */}
            <div 
              className="rounded-2xl p-5 shadow-sm"
              style={{ backgroundColor: isDark ? '#1E2527' : '#FFFFFF' }}
            >
              <h3 className="font-medium mb-4 flex items-center gap-2">
                <span style={{ color: colors.primary }}>💾</span>
                磁盘信息
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {state.disks.map((disk) => (
                  <div 
                    key={disk.letter}
                    className="p-4 rounded-xl"
                    style={{ backgroundColor: isDark ? '#252B2D' : '#F8F8F8' }}
                  >
                    <DiskInfoItem disk={disk} />
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div 
            className="rounded-2xl p-5 shadow-sm"
            style={{ backgroundColor: isDark ? '#1E2527' : '#FFFFFF' }}
          >
            <h3 className="font-medium mb-6 flex items-center gap-2">
              <span style={{ color: colors.primary }}>⚙️</span>
              设置
            </h3>
            
            <div className="space-y-6">
              {/* 语言设置 */}
              <div>
                <label className="block text-sm mb-2 opacity-70">语言</label>
                <select 
                  className="w-full p-3 rounded-xl border-0 outline-none transition-all"
                  style={{ backgroundColor: isDark ? '#252B2D' : '#F0F0F0', color: textColor }}
                  value={state.settings.language}
                  onChange={(e) => changeLanguage(e.target.value)}
                >
                  <option value="zh-CN">简体中文</option>
                  <option value="en-US">English</option>
                </select>
              </div>

              {/* 主题设置 */}
              <div>
                <label className="block text-sm mb-2 opacity-70">主题</label>
                <div className="flex gap-3">
                  <button 
                    onClick={() => state.settings.theme === 'dark' && toggleTheme()}
                    className={`flex-1 py-3 rounded-xl transition-all ${state.settings.theme === 'light' ? 'text-white' : ''}`}
                    style={{ backgroundColor: state.settings.theme === 'light' ? colors.primary : (isDark ? '#252B2D' : '#F0F0F0') }}
                  >
                    ☀️ 浅色
                  </button>
                  <button 
                    onClick={() => state.settings.theme === 'light' && toggleTheme()}
                    className={`flex-1 py-3 rounded-xl transition-all ${state.settings.theme === 'dark' ? 'text-white' : ''}`}
                    style={{ backgroundColor: state.settings.theme === 'dark' ? colors.primary : (isDark ? '#252B2D' : '#F0F0F0') }}
                  >
                    🌙 深色
                  </button>
                </div>
              </div>

              {/* 自动清理 */}
              <div className="flex items-center justify-between py-3">
                <div>
                  <div className="font-medium">自动清理</div>
                  <div className="text-sm opacity-60">每周自动扫描并清理</div>
                </div>
                <button
                  className="w-12 h-6 rounded-full transition-all relative"
                  style={{ backgroundColor: state.settings.autoStart ? colors.primary : '#CCC' }}
                  onClick={() => {}}
                >
                  <div 
                    className="absolute top-1 w-4 h-4 rounded-full bg-white transition-all"
                    style={{ left: state.settings.autoStart ? 'calc(100% - 1.25rem)' : '0.25rem' }}
                  />
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

// 应用入口组件
function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  )
}

export default App
