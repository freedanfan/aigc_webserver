import { get, post, del } from '@/utils/request'
import { ResponseData, GenerateImageParams, GeneratedImage, PaginationResult } from '../types'
import { USE_MOCK } from '@/utils/config'

/**
 * 生成模拟图片数据
 * @param count 需要生成的图片数量
 * @returns 模拟的图片数据数组
 */
const generateMockImages = (count: number = 1): GeneratedImage[] => {
  return Array(count).fill(0).map((_, index) => ({
    id: Date.now() + index,
    url: `https://picsum.photos/400/300?random=${Math.random()}`,
    title: `生成图片 ${index + 1}`,
    createdAt: new Date().toISOString()
  }))
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
 * 图片生成相关接口
 * 包含图片生成、上传、查询和删除等功能
 */
export default {
  /**
   * 生成图片
   * 根据提供的提示词和参数生成图片
   * @param params 图片生成参数，包含提示词、风格、色彩等
   * @returns 返回生成的图片列表
   */
  generateImage(params: GenerateImageParams): Promise<ResponseData<GeneratedImage[]>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据生成图片，参数：', params)
      
      // 获取要生成的图片数量，默认为 1
      const count = params.count || 1
      
      // 是否需要优化提示词
      const needOptimize = params.need_optimize_prompt === 1
      
      // 记录优化状态
      const optimizeStatus = needOptimize ? '已优化' : '未优化'
      
      // 模拟网络延迟，根据图片数量增加延迟时间
      const delay = 1000 + count * 500 // 基础延迟 1 秒，每张图片增加 0.5 秒
      
      return new Promise(resolve => {
        setTimeout(() => {
          // 生成模拟图片，并在标题中添加优化状态
          const images = generateMockImages(count).map(img => ({
            ...img,
            title: `${img.title} (${optimizeStatus})`
          }))
          
          resolve(createMockResponse(images))
        }, delay)
      })
    }
    
    // 否则调用真实 API
    return post('/image/generate', params)
  },
  
  /**
   * 获取历史生成的图片
   * 分页查询用户生成过的图片
   * @param page 页码，默认为第 1 页
   * @param pageSize 每页数量，默认为 10 条
   * @returns 返回分页的图片列表和分页信息
   */
  getHistoryImages(page = 1, pageSize = 10): Promise<ResponseData<PaginationResult<GeneratedImage>>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据获取历史图片，页码：', page, '每页数量：', pageSize)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse({
            list: generateMockImages(pageSize),
            total: 100,
            page,
            pageSize
          }))
        }, 800)
      })
    }
    
    // 否则调用真实 API
    return get('/image/history', { page, pageSize })
  },
  
  /**
   * 上传参考图片
   * 用于上传用户提供的参考图片，作为生成图片的参考
   * @param file 要上传的图片文件
   * @returns 返回上传后的图片 URL
   */
  uploadReferenceImage(file: File): Promise<ResponseData<{ url: string }>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据上传图片，文件名：', file.name)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse({
            url: `https://picsum.photos/400/300?random=${Math.random()}`
          }))
        }, 1200)
      })
    }
    
    // 创建 FormData 对象，用于文件上传
    const formData = new FormData()
    formData.append('file', file)
    
    // 发送 POST 请求，设置正确的 Content-Type
    return post('/image/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  /**
   * 删除生成的图片
   * @param id 要删除的图片 ID
   * @returns 返回删除结果
   */
  deleteImage(id: number): Promise<ResponseData<null>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据删除图片，ID：', id)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse(null))
        }, 500)
      })
    }
    
    // 否则调用真实 API
    return del(`/image/${id}`)
  },
  
  /**
   * 获取单张图片详情
   * @param id 图片 ID
   * @returns 返回图片详细信息
   */
  getImageDetail(id: number): Promise<ResponseData<GeneratedImage>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据获取图片详情，ID：', id)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse({
            id,
            url: `https://picsum.photos/400/300?random=${Math.random()}`,
            title: `图片详情 ${id}`,
            createdAt: new Date().toISOString()
          }))
        }, 600)
      })
    }
    
    // 否则调用真实 API
    return get(`/image/${id}`)
  },
  
  /**
   * 获取推荐图片
   * 获取系统推荐的图片，可用于首页展示
   * @param limit 返回的图片数量，默认为 4 张
   * @returns 返回推荐的图片列表
   */
  getRecommendImages(limit = 4): Promise<ResponseData<GeneratedImage[]>> {
    // 如果使用模拟数据，则返回模拟数据
    if (USE_MOCK) {
      console.log('使用模拟数据获取推荐图片，数量：', limit)
      // 模拟网络延迟
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(createMockResponse(generateMockImages(limit)))
        }, 700)
      })
    }
    
    // 否则调用真实 API
    return get('/image/recommend', { limit })
  }
} 