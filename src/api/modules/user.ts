import { get, post } from '@/utils/request'
import { ResponseData, User, LoginParams, LoginResult } from '../types'

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
    return post('/api/user/login', params)
  },
  
  /**
   * 获取当前登录用户的信息
   * 需要在请求头中携带 token
   * @returns 返回用户信息
   */
  getUserInfo(): Promise<ResponseData<User>> {
    return get('/api/user/info')
  },
  
  /**
   * 用户登出
   * 清除服务器端的登录状态
   * @returns 返回登出结果
   */
  logout(): Promise<ResponseData<null>> {
    return post('/api/user/logout')
  },
  
  /**
   * 用户注册
   * @param params 注册参数，包含用户名、密码和邮箱
   * @returns 返回注册结果，包含 token 和用户信息
   */
  register(params: LoginParams & { email: string }): Promise<ResponseData<LoginResult>> {
    return post('/api/user/register', params)
  },
  
  /**
   * 修改用户信息
   * @param params 要修改的用户信息字段
   * @returns 返回更新后的用户信息
   */
  updateUserInfo(params: Partial<User>): Promise<ResponseData<User>> {
    return post('/api/user/update', params)
  },
  
  /**
   * 修改用户密码
   * @param params 包含旧密码和新密码
   * @returns 返回修改结果
   */
  changePassword(params: { oldPassword: string; newPassword: string }): Promise<ResponseData<null>> {
    return post('/api/user/change-password', params)
  }
} 