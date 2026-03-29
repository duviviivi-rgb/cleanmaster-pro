// Provider组件
export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // 加载磁盘信息
  const loadDisks = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: { disks: true } });
      const disks = await diskApi.getDisks();
      dispatch({ type: 'SET_DISKS', payload: disks });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '加载磁盘信息失败' });
      dispatch({ type: 'SET_LOADING', payload: { disks: false } });
      // 使用模拟数据
      const mockDisks = [
        {
          letter: 'C:',
          name: '系统盘',
          totalSpace: 135000000000,
          usedSpace: 100000000000,
          freeSpace: 35000000000,
          percentage: 74,
        },
        {
          letter: 'D:',
          name: '数据盘',
          totalSpace: 500000000000,
          usedSpace: 150000000000,
          freeSpace: 350000000000,
          percentage: 30,
        },
        {
          letter: 'E:',
          name: '娱乐盘',
          totalSpace: 250000000000,
          usedSpace: 50000000000,
          freeSpace: 200000000000,
          percentage: 20,
        },
      ];
      dispatch({ type: 'SET_DISKS', payload: mockDisks });
    }
  };

  // 加载用户设置
  const loadSettings = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: { settings: true } });
      const settings = await settingsApi.getSettings();
      dispatch({ type: 'SET_SETTINGS', payload: settings });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '加载设置失败' });
      dispatch({ type: 'SET_LOADING', payload: { settings: false } });
      // 使用默认设置
    }
  };

  // 初始化加载
  useEffect(() => {
    loadDisks();
    loadSettings();
  }, []);

  const value: AppContextType = {
    state,
    dispatch,
    loadDisks,
    loadSettings,
    saveSettings,
    toggleTheme,
    changeLanguage,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}// Provider组件
export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // 加载磁盘信息
  const loadDisks = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: { disks: true } });
      const disks = await diskApi.getDisks();
      dispatch({ type: 'SET_DISKS', payload: disks });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '加载磁盘信息失败' });
      dispatch({ type: 'SET_LOADING', payload: { disks: false } });
      // 使用模拟数据
      const mockDisks = [
        {
          letter: 'C:',
          name: '系统盘',
          totalSpace: 135000000000,
          usedSpace: 100000000000,
          freeSpace: 35000000000,
          percentage: 74,
        },
        {
          letter: 'D:',
          name: '数据盘',
          totalSpace: 500000000000,
          usedSpace: 150000000000,
          freeSpace: 350000000000,
          percentage: 30,
        },
        {
          letter: 'E:',
          name: '娱乐盘',
          totalSpace: 250000000000,
          usedSpace: 50000000000,
          freeSpace: 200000000000,
          percentage: 20,
        },
      ];
      dispatch({ type: 'SET_DISKS', payload: mockDisks });
    }
  };

  // 加载用户设置
  const loadSettings = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: { settings: true } });
      const settings = await settingsApi.getSettings();
      dispatch({ type: 'SET_SETTINGS', payload: settings });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '加载设置失败' });
      dispatch({ type: 'SET_LOADING', payload: { settings: false } });
      // 使用默认设置
    }
  };

  // 初始化加载
  useEffect(() => {
    loadDisks();
    loadSettings();
  }, []);

  const value: AppContextType = {
    state,
    dispatch,
    loadDisks,
    loadSettings,
    saveSettings,
    toggleTheme,
    changeLanguage,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}// Provider组件
export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // 加载磁盘信息
  const loadDisks = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: { disks: true } });
      const disks = await diskApi.getDisks();
      dispatch({ type: 'SET_DISKS', payload: disks });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '加载磁盘信息失败' });
      dispatch({ type: 'SET_LOADING', payload: { disks: false } });
      // 使用模拟数据
      const mockDisks = [
        {
          letter: 'C:',
          name: '系统盘',
          totalSpace: 135000000000,
          usedSpace: 100000000000,
          freeSpace: 35000000000,
          percentage: 74,
        },
        {
          letter: 'D:',
          name: '数据盘',
          totalSpace: 500000000000,
          usedSpace: 150000000000,
          freeSpace: 350000000000,
          percentage: 30,
        },
        {
          letter: 'E:',
          name: '娱乐盘',
          totalSpace: 250000000000,
          usedSpace: 50000000000,
          freeSpace: 200000000000,
          percentage: 20,
        },
      ];
      dispatch({ type: 'SET_DISKS', payload: mockDisks });
    }
  };

  // 加载用户设置
  const loadSettings = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: { settings: true } });
      const settings = await settingsApi.getSettings();
      dispatch({ type: 'SET_SETTINGS', payload: settings });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '加载设置失败' });
      dispatch({ type: 'SET_LOADING', payload: { settings: false } });
      // 使用默认设置
    }
  };

  // 初始化加载
  useEffect(() => {
    loadDisks();
    loadSettings();
  }, []);

  const value: AppContextType = {
    state,
    dispatch,
    loadDisks,
    loadSettings,
    saveSettings,
    toggleTheme,
    changeLanguage,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Text.Json;
using CleanMasterPro.Models;

namespace CleanMasterPro.Services
{
    public class ApiServer
    {
        private HttpListener listener;
        private readonly int port;
        private readonly DiskService diskService;
        private readonly ScanService scanService;
        private readonly CleanService cleanService;
        private readonly SettingsService settingsService;
        private readonly HistoryService historyService;
        private readonly LocalizationService localizationService;

        public ApiServer(int port = 5000)
        {
            this.port = port;
            this.diskService = new DiskService();
            this.scanService = new ScanService();
            this.cleanService = new CleanService();
            this.settingsService = new SettingsService();
            this.historyService = new HistoryService();
            this.localizationService = new LocalizationService();
        }

        public void Start()
        {
            try
            {
                listener = new HttpListener();
                listener.Prefixes.Add($"http://localhost:{port}/api/");
                listener.Start();
                Console.WriteLine($"API服务器已启动，监听端口: {port}");

                // 异步处理请求
                listener.BeginGetContext(new AsyncCallback(HandleRequest), listener);
            }
            catch (HttpListenerException ex)
            {
                Console.WriteLine($"启动API服务器失败: {ex.Message}");
                Console.WriteLine("可能的原因:");
                Console.WriteLine("1. 端口 {port} 已被占用");
                Console.WriteLine("2. 应用没有管理员权限");
                Console.WriteLine("3. 防火墙阻止了连接");
                throw;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"启动API服务器失败: {ex.Message}");
                throw;
            }
        }

        public void Stop()
        {
            listener?.Stop();
            Console.WriteLine("API服务器已停止");
        }

        private void HandleRequest(IAsyncResult result)
        {
            var listener = (HttpListener)result.AsyncState;
            HttpListenerContext context = null;

            try
            {
                context = listener.EndGetContext(result);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"获取请求上下文失败: {ex.Message}");
            }
            finally
            {
                // 继续监听下一个请求
                listener.BeginGetContext(new AsyncCallback(HandleRequest), listener);
            }

            if (context == null)
            {
                return;
            }

            var request = context.Request;
            var response = context.Response;

            try
            {
                // 处理CORS
                response.AddHeader("Access-Control-Allow-Origin", "*");
                response.AddHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
                response.AddHeader("Access-Control-Allow-Headers", "Content-Type");

                // 处理OPTIONS请求
                if (request.HttpMethod == "OPTIONS")
                {
                    response.StatusCode = (int)HttpStatusCode.OK;
                    response.Close();
                    return;
                }

                // 解析请求路径
                var path = request.Url.AbsolutePath.Replace("/api", "");

                // 处理不同的API端点
                if (path.StartsWith("/disk"))
                {
                    HandleDiskRequest(response);
                }
                else if (path.StartsWith("/scan/quick"))
                {
                    var disk = request.QueryString["disk"] ?? "C:";
                    HandleQuickScanRequest(response, disk);
                }
                else if (path.StartsWith("/scan/deep"))
                {
                    var disk = request.QueryString["disk"] ?? "C:";
                    HandleDeepScanRequest(response, disk);
                }
                else if (path.StartsWith("/scan/analysis"))
                {
                    var disk = request.QueryString["disk"] ?? "C:";
                    HandleIntelligentAnalysisRequest(response, disk);
                }
                else if (path.StartsWith("/clean/execute"))
                {
                    HandleCleanExecuteRequest(request, response);
                }
                else if (path.StartsWith("/clean/auto"))
                {
                    HandleAutoCleanRequest(request, response);
                }
                else if (path.StartsWith("/settings"))
                {
                    if (request.HttpMethod == "GET")
                    {
                        HandleGetSettingsRequest(response);
                    }
                    else if (request.HttpMethod == "POST")
                    {
                        HandleSaveSettingsRequest(request, response);
                    }
                }
                else if (path.StartsWith("/history"))
                {
                    HandleGetHistoryRequest(response);
                }
                else
                {
                    response.StatusCode = (int)HttpStatusCode.NotFound;
                    response.Close();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"处理请求失败: {ex.Message}");
                try
                {
                    response.StatusCode = (int)HttpStatusCode.InternalServerError;
                    response.Close();
                }
                catch { }
            }
        }

        private void HandleDiskRequest(HttpListenerResponse response)
        {
            var disks = diskService.GetDisks();
            SendResponse(response, disks);
        }

        private void HandleQuickScanRequest(HttpListenerResponse response, string disk)
        {
            var result = scanService.QuickScan(disk);
            SendResponse(response, result);
        }

        private void HandleDeepScanRequest(HttpListenerResponse response, string disk)
        {
            var result = scanService.DeepScan(disk);
            SendResponse(response, result);
        }

        private void HandleIntelligentAnalysisRequest(HttpListenerResponse response, string disk)
        {
            var result = scanService.IntelligentAnalysis(disk);
            SendResponse(response, result);
        }

        private void HandleCleanExecuteRequest(HttpListenerRequest request, HttpListenerResponse response)
        {
            using (var reader = new StreamReader(request.InputStream))
            {
                var json = reader.ReadToEnd();
                var data = JsonSerializer.Deserialize<CleanRequest>(json);
                var result = cleanService.ExecuteClean(data.Files, data.Disk);
                SendResponse(response, result);
            }
        }

        private void HandleAutoCleanRequest(HttpListenerRequest request, HttpListenerResponse response)
        {
            using (var reader = new StreamReader(request.InputStream))
            {
                var json = reader.ReadToEnd();
                var settings = JsonSerializer.Deserialize<AutoCleanSettings>(json);
                var result = cleanService.SetAutoClean(settings);
                SendResponse(response, new { success = result });
            }
        }

        private void HandleGetSettingsRequest(HttpListenerResponse response)
        {
            var settings = settingsService.GetSettings();
            SendResponse(response, settings);
        }

        private void HandleSaveSettingsRequest(HttpListenerRequest request, HttpListenerResponse response)
        {
            using (var reader = new StreamReader(request.InputStream))
            {
                var json = reader.ReadToEnd();
                var settings = JsonSerializer.Deserialize<UserSettings>(json);
                var result = settingsService.SaveSettings(settings);
                SendResponse(response, new { success = result });
            }
        }

        private void HandleGetHistoryRequest(HttpListenerResponse response)
        {
            var history = historyService.GetCleanHistory();
            SendResponse(response, history);
        }

        private void SendResponse(HttpListenerResponse response, object data)
        {
            try
            {
                var json = JsonSerializer.Serialize(data);
                var buffer = Encoding.UTF8.GetBytes(json);
                
                response.ContentType = "application/json";
                response.ContentLength64 = buffer.Length;
                response.StatusCode = (int)HttpStatusCode.OK;
                
                using (var output = response.OutputStream)
                {
                    output.Write(buffer, 0, buffer.Length);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"发送响应失败: {ex.Message}");
                response.StatusCode = (int)HttpStatusCode.InternalServerError;
            }
            finally
            {
                response.Close();
            }
        }
    }

    public class CleanRequest
    {
        public string[] Files { get; set; }
        public string Disk { get; set; }
    }
}
