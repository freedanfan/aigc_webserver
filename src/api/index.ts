/**
 * API 模块入口文件
 * 统一导出所有 API 模块，方便在组件中引用
 */

// 导入各个功能模块的 API
import userApi from './modules/user'
import imageApi from './modules/image'

/**
 * 导出所有 API 模块
 * 可以通过 import { userApi, imageApi } from '@/api' 的方式导入
 */
export {
  userApi,
  imageApi
}

/**
 * 导出所有类型定义
 * 可以通过 import { ResponseData, User, ... } from '@/api' 的方式导入
 */
export * from './types'

/**
 * 默认导出所有 API
 * 可以通过 import api from '@/api' 的方式导入，然后通过 api.user.xxx 调用
 */
export default {
  user: userApi,
  image: imageApi
} 