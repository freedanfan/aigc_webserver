import axios, { AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { message } from 'ant-design-vue'
import { API_BASE_URL, API_PREFIX, getApiUrl } from '@/utils/config'

/**
 * 创建 axios 实例
 * 配置基础URL、超时时间和默认请求头
 */
const service = axios.create({
  baseURL: API_BASE_URL, // 使用环境变量中的 API 基础 URL
  timeout: 15000, // 请求超时时间，单位毫秒
  headers: {
    'Content-Type': 'application/json;charset=utf-8' // 默认请求头
  }
})

/**
 * 请求拦截器
 * 在发送请求之前做一些处理，例如添加 token、处理请求参数等
 */
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 从本地存储获取 token
    const token = localStorage.getItem('token')
    // 如果 token 存在，则添加到请求头中
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 如果 URL 不是以 http 开头，并且不是以 API 前缀开头，则添加 API 前缀
    if (config.url && !config.url.startsWith('http') && !config.url.startsWith(API_PREFIX)) {
      config.url = `${API_PREFIX}${config.url}`
    }
    
    return config
  },
  (error: AxiosError) => {
    // 请求错误处理
    console.error('请求错误：', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * 在接收到响应后做一些处理，例如统一处理错误、格式化响应数据等
 */
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response
    
    // 根据自定义错误码判断请求是否成功
    // 这里假设后端返回的数据格式为 { code: number, data: any, message: string }
    if (data.code && data.code !== 200) {
      // 处理业务错误，例如参数错误、权限不足等
      console.error('业务错误：', data.message || '未知错误')
      return Promise.reject(new Error(data.message || '未知错误'))
    }
    
    // 请求成功返回数据
    return data
  },
  (error: AxiosError) => {
    // 处理 HTTP 错误，例如 404、500 等
    let messageText = '网络错误，请稍后重试'
    
    // 检查是否是连接被拒绝错误（后端服务不可用）
    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      messageText = '无法连接到服务器，请检查后端服务是否启动'
      console.error('后端服务连接失败：', error)
      // 显示全局提示，但不重复显示
      message.error(messageText, 3)
      return Promise.reject(error)
    }
    
    if (error.response) {
      // 请求已发出，但服务器响应的状态码不在 2xx 范围内
      const status = error.response.status
      
      // 根据状态码定制错误信息
      switch (status) {
        case 400:
          messageText = '请求错误' // Bad Request
          break
        case 401:
          messageText = '未授权，请重新登录' // Unauthorized
          // 可以在这里处理登出逻辑，例如清除本地存储的 token、跳转到登录页等
          // store.dispatch('user/logout')
          break
        case 403:
          messageText = '拒绝访问' // Forbidden
          break
        case 404:
          messageText = '请求的资源不存在' // Not Found
          break
        case 500:
          messageText = '服务器错误' // Internal Server Error
          break
        default:
          messageText = `请求错误 (${status})`
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      messageText = '服务器无响应'
    }
    
    console.error('响应错误：', messageText)
    // 显示全局提示
    message.error(messageText, 3)
    return Promise.reject(error)
  }
)

/**
 * 封装 GET 请求
 * @param url 请求地址
 * @param params 请求参数，会被添加到 URL 中
 * @param config 其他配置项
 * @returns Promise 对象
 */
export function get<T>(url: string, params?: any, config = {}): Promise<T> {
  // 使用 getApiUrl 处理 URL
  const fullUrl = getApiUrl(url)
  
  return service.get(fullUrl, { params, ...config })
    .then(response => response as unknown as T)
    .catch(error => {
      // 在这里可以添加特定于 GET 请求的错误处理
      return Promise.reject(error)
    })
}

/**
 * 封装 POST 请求
 * @param url 请求地址
 * @param data 请求体数据
 * @param config 其他配置项
 * @returns Promise 对象
 */
export function post<T>(url: string, data?: any, config = {}): Promise<T> {
  // 使用 getApiUrl 处理 URL
  const fullUrl = getApiUrl(url)
  
  return service.post(fullUrl, data, config)
    .then(response => response as unknown as T)
    .catch(error => {
      // 在这里可以添加特定于 POST 请求的错误处理
      return Promise.reject(error)
    })
}

/**
 * 封装 PUT 请求
 * @param url 请求地址
 * @param data 请求体数据
 * @param config 其他配置项
 * @returns Promise 对象
 */
export function put<T>(url: string, data?: any, config = {}): Promise<T> {
  // 使用 getApiUrl 处理 URL
  const fullUrl = getApiUrl(url)
  
  return service.put(fullUrl, data, config)
    .then(response => response as unknown as T)
    .catch(error => {
      // 在这里可以添加特定于 PUT 请求的错误处理
      return Promise.reject(error)
    })
}

/**
 * 封装 DELETE 请求
 * @param url 请求地址
 * @param config 其他配置项
 * @returns Promise 对象
 */
export function del<T>(url: string, config = {}): Promise<T> {
  // 使用 getApiUrl 处理 URL
  const fullUrl = getApiUrl(url)
  
  return service.delete(fullUrl, config)
    .then(response => response as unknown as T)
    .catch(error => {
      // 在这里可以添加特定于 DELETE 请求的错误处理
      return Promise.reject(error)
    })
}

// 导出 axios 实例，以便在特殊情况下可以直接使用
export default service 