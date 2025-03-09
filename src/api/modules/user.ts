import { get, post } from '@/utils/request'
import { ResponseData, User, LoginParams, LoginResult } from '../types'
import { USE_MOCK } from '@/utils/config'

/**
 * 模拟用户数据
 */
const mockUser: User = {
  id: 1,
  username: 'demo_user',
  email: 'demo@example.com',
  avatar: 'https://randomuser.me/api/portraits/lego/1.jpg'
}

/**
 * 创建模拟响应
 * @param data 响应数据
 * @returns 模拟的响应对象
 */
const createMockResponse = <T>(data: T): ResponseData<T> => {
  return {
    code: 200,
    data,
    message: '操作成功'
  }
}

/**
 * 用户相关接口
 * 包含用户登录、注册、获取用户信息等功能
 */
export default {
  /**
   * 用户登录
   * @param params 登录参数，包含用户名和密码
   * @returns 返回登录结果，包含 token 和用户信息
   */
  login(params: LoginParams): Promise<ResponseData<LoginResult>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据登录，参数：', params)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse({
            token: 'mock_token_' + Date.now(),
            user: mockUser
          }))
        }, 800)
      })
    }
    
    // 否则调用真实 API
    return post('/user/login', params)
  },
  
  /**
   * 获取当前登录用户的信息
   * 需要在请求头中携带 token
   * @returns 返回用户信息
   */
  getUserInfo(): Promise<ResponseData<User>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据获取用户信息')
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse(mockUser))
        }, 600)
      })
    }
    
    // 否则调用真实 API
    return get('/user/info')
  },
  
  /**
   * 用户登出
   * 清除服务器端的登录状态
   * @returns 返回登出结果
   */
  logout(): Promise<ResponseData<null>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据登出')
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse(null))
        }, 500)
      })
    }
    
    // 否则调用真实 API
    return post('/user/logout')
  },
  
  /**
   * 用户注册
   * @param params 注册参数，包含用户名、密码和邮箱
   * @returns 返回注册结果，包含 token 和用户信息
   */
  register(params: LoginParams & { email: string }): Promise<ResponseData<LoginResult>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据注册，参数：', params)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse({
            token: 'mock_token_' + Date.now(),
            user: {
              ...mockUser,
              username: params.username,
              email: params.email
            }
          }))
        }, 1000)
      })
    }
    
    // 否则调用真实 API
    return post('/user/register', params)
  },
  
  /**
   * 修改用户信息
   * @param params 要修改的用户信息字段
   * @returns 返回更新后的用户信息
   */
  updateUserInfo(params: Partial<User>): Promise<ResponseData<User>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据更新用户信息，参数：', params)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse({
            ...mockUser,
            ...params
          }))
        }, 700)
      })
    }
    
    // 否则调用真实 API
    return post('/user/update', params)
  },
  
  /**
   * 修改用户密码
   * @param params 包含旧密码和新密码
   * @returns 返回修改结果
   */
  changePassword(params: { oldPassword: string; newPassword: string }): Promise<ResponseData<null>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据修改密码，参数：', params)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse(null))
        }, 800)
      })
    }
    
    // 否则调用真实 API
    return post('/user/change-password', params)
  }
} 