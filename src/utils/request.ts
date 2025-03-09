import axios, { AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios'

/**
 * 创建 axios 实例
 * 配置基础URL、超时时间和默认请求头
 */
const service = axios.create({
  baseURL: '', // 如果所有请求都已经通过 Vite 代理，这里可以为空
  timeout: 200000, // 请求超时时间，单位毫秒
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
    let message = '网络错误，请稍后重试'
    
    if (error.response) {
      // 请求已发出，但服务器响应的状态码不在 2xx 范围内
      const status = error.response.status
      
      // 根据状态码定制错误信息
      switch (status) {
        case 400:
          message = '请求错误' // Bad Request
          break
        case 401:
          message = '未授权，请重新登录' // Unauthorized
          // 可以在这里处理登出逻辑，例如清除本地存储的 token、跳转到登录页等
          // store.dispatch('user/logout')
          break
        case 403:
          message = '拒绝访问' // Forbidden
          break
        case 404:
          message = '请求的资源不存在' // Not Found
          break
        case 500:
          message = '服务器错误' // Internal Server Error
          break
        default:
          message = `请求错误 (${status})`
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      message = '服务器无响应'
    }
    
    console.error('响应错误：', message)
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
  return service.get(url, { params, ...config })
}

/**
 * 封装 POST 请求
 * @param url 请求地址
 * @param data 请求体数据
 * @param config 其他配置项
 * @returns Promise 对象
 */
export function post<T>(url: string, data?: any, config = {}): Promise<T> {
  return service.post(url, data, config)
}

/**
 * 封装 PUT 请求
 * @param url 请求地址
 * @param data 请求体数据
 * @param config 其他配置项
 * @returns Promise 对象
 */
export function put<T>(url: string, data?: any, config = {}): Promise<T> {
  return service.put(url, data, config)
}

/**
 * 封装 DELETE 请求
 * @param url 请求地址
 * @param config 其他配置项
 * @returns Promise 对象
 */
export function del<T>(url: string, config = {}): Promise<T> {
  return service.delete(url, config)
}

// 导出 axios 实例，以便在特殊情况下可以直接使用
export default service 