import { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';
import { diskApi, settingsApi } from '../services/api';
import type { Language } from '../i18n';

// 状态类型定义
interface AppState {
  // 磁盘信息
  disks: Array<{
    letter: string;
    name: string;
    totalSpace: number;
    usedSpace: number;
    freeSpace: number;
    percentage: number;
  }>;
  // 用户设置
  settings: {
    language: Language;
    theme: 'light' | 'dark';
    autoStart: boolean;
    defaultCleanLevel: 'standard' | 'deep' | 'custom';
    historyRetention: number;
  };
  // 加载状态
  loading: {
    disks: boolean;
    settings: boolean;
  };
  // 错误信息
  error: string | null;
}

// 初始状态
const initialState: AppState = {
  disks: [],
  settings: {
    language: 'zh-CN' as Language,
    theme: 'light',
    autoStart: false,
    defaultCleanLevel: 'standard',
    historyRetention: 30,
  },
  loading: {
    disks: false,
    settings: false,
  },
  error: null,
};

// Action类型
type AppAction =
  | { type: 'SET_DISKS'; payload: AppState['disks'] }
  | { type: 'SET_SETTINGS'; payload: AppState['settings'] }
  | { type: 'SET_LOADING'; payload: Partial<AppState['loading']> }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_THEME'; payload: 'light' | 'dark' }
  | { type: 'SET_LANGUAGE'; payload: Language };

// Reducer函数
function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_DISKS':
      return {
        ...state,
        disks: action.payload,
        loading: {
          ...state.loading,
          disks: false,
        },
      };
    case 'SET_SETTINGS':
      return {
        ...state,
        settings: action.payload,
        loading: {
          ...state.loading,
          settings: false,
        },
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: {
          ...state.loading,
          ...action.payload,
        },
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    case 'SET_THEME':
      return {
        ...state,
        settings: {
          ...state.settings,
          theme: action.payload,
        },
      };
    case 'SET_LANGUAGE':
      return {
        ...state,
        settings: {
          ...state.settings,
          language: action.payload,
        },
      };
    default:
      return state;
  }
}

// Context类型
interface AppContextType {
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
  // 辅助函数
  loadDisks: () => Promise<void>;
  loadSettings: () => Promise<void>;
  saveSettings: (settings: Partial<AppState['settings']>) => Promise<void>;
  toggleTheme: () => void;
  changeLanguage: (language: string) => void;
}

// 创建Context
const AppContext = createContext<AppContextType | undefined>(undefined);

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
      console.error('加载磁盘信息失败:', error);
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
      dispatch({ type: 'SET_SETTINGS', payload: { ...settings, language: settings.language as Language } });
    } catch (error) {
      console.error('加载设置失败:', error);
      dispatch({ type: 'SET_ERROR', payload: '加载设置失败' });
      dispatch({ type: 'SET_LOADING', payload: { settings: false } });
      // 使用默认设置
      const defaultSettings = {
        language: 'zh-CN' as Language,
        theme: 'light' as const,
        autoStart: false,
        defaultCleanLevel: 'standard' as const,
        historyRetention: 30,
      };
      dispatch({ type: 'SET_SETTINGS', payload: defaultSettings });
    }
  };

  // 保存用户设置
  const saveSettings = async (newSettings: Partial<AppState['settings']>) => {
    try {
      const updatedSettings = { ...state.settings, ...newSettings };
      await settingsApi.saveSettings(updatedSettings);
      dispatch({ type: 'SET_SETTINGS', payload: updatedSettings });
    } catch (error) {
      console.error('保存设置失败:', error);
      dispatch({ type: 'SET_ERROR', payload: '保存设置失败' });
    }
  };

  // 切换主题
  const toggleTheme = () => {
    const newTheme = state.settings.theme === 'light' ? 'dark' : 'light';
    dispatch({ type: 'SET_THEME', payload: newTheme });
    saveSettings({ theme: newTheme });
  };

  // 更改语言
  const changeLanguage = (language: string) => {
    dispatch({ type: 'SET_LANGUAGE', payload: language as Language });
    saveSettings({ language: language as Language });
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
}

// 自定义Hook
export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}