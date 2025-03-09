/**
 * 配置工具
 * 用于获取环境变量和应用配置
 */

// 环境变量
export const ENV = import.meta.env.VITE_APP_ENV || 'development'
export const IS_DEV = ENV === 'development'
export const IS_TEST = ENV === 'test'
export const IS_PROD = ENV === 'production'
export const APP_TITLE = import.meta.env.VITE_APP_TITLE
export const APP_VERSION = import.meta.env.VITE_APP_VERSION
export const DEBUG = import.meta.env.VITE_APP_DEBUG === 'true'

// API 配置
export const API_BASE_URL = import.meta.env.VITE_APP_API_BASE_URL || ''
export const API_PREFIX = import.meta.env.VITE_APP_API_PREFIX || '/api'
export const USE_MOCK = import.meta.env.VITE_APP_USE_MOCK === 'true'

// 完整的 API URL
export const getApiUrl = (path: string): string => {
  // 如果路径已经是完整的 URL，则直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  
  // 确保路径以 / 开头
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  
  // 如果路径已经包含 API 前缀，则不再添加
  if (normalizedPath.startsWith(API_PREFIX)) {
    return `${API_BASE_URL}${normalizedPath}`
  }
  
  // 否则添加 API 前缀
  return `${API_BASE_URL}${API_PREFIX}${normalizedPath}`
}

// 导出配置对象
export default {
  env: ENV,
  isDev: IS_DEV,
  isTest: IS_TEST,
  isProd: IS_PROD,
  appTitle: APP_TITLE,
  appVersion: APP_VERSION,
  debug: DEBUG,
  apiBaseUrl: API_BASE_URL,
  apiPrefix: API_PREFIX,
  useMock: USE_MOCK,
  getApiUrl
} 