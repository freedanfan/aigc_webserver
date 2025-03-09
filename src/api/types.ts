/**
 * 定义接口返回数据的通用类型
 * 后端返回的数据统一格式
 */
export interface ResponseData<T = any> {
  /** 状态码，200 表示成功 */
  code: number
  /** 实际返回的数据 */
  data: T
  /** 状态信息，一般在错误时使用 */
  message: string
}

/**
 * 用户信息接口
 * 包含用户的基本信息
 */
export interface User {
  /** 用户唯一标识 */
  id: number
  /** 用户名 */
  username: string
  /** 用户邮箱 */
  email: string
  /** 用户头像地址，可选 */
  avatar?: string
}

/**
 * 登录请求参数接口
 */
export interface LoginParams {
  /** 用户名 */
  username: string
  /** 密码 */
  password: string
}

/**
 * 登录成功后返回的数据接口
 */
export interface LoginResult {
  /** JWT token，用于后续请求的身份验证 */
  token: string
  /** 用户信息 */
  user: User
}

/**
 * 图片生成请求参数接口
 */
export interface GenerateImageParams {
  /** 正向提示词，描述想要生成的图片内容（必填） */
  prompt: string
  /** 反向提示词，描述不想在图片中出现的内容，可选 */
  negativePrompt?: string
  /** 图片风格，可选 */
  stylePrompt?: string
  /** 图片色彩，可选 */
  colorPrompt?: string
  /** 图片光照，可选 */
  lightPrompt?: string
  /** 图片构图，可选 */
  compositionPrompt?: string
  /** 参考图片的 base64 编码，可选 */
  referenceImage?: string
  /** 生成图片数量，默认为 1 */
  count?: number
  /** 是否需要优化提示词，1表示是，0表示否 */
  need_optimize_prompt?: number
}

/**
 * 生成的图片信息接口
 */
export interface GeneratedImage {
  /** 图片唯一标识 */
  id: number
  /** 图片 URL 地址 */
  url: string
  /** 图片标题 */
  title: string
  /** 图片创建时间 */
  createdAt: string
}

/**
 * 分页查询参数接口
 */
export interface PaginationParams {
  /** 当前页码，从 1 开始 */
  page: number
  /** 每页数据条数 */
  pageSize: number
}

/**
 * 分页查询结果接口
 * 包含分页数据和分页信息
 */
export interface PaginationResult<T> {
  /** 当前页的数据列表 */
  list: T[]
  /** 总数据条数 */
  total: number
  /** 当前页码 */
  page: number
  /** 每页数据条数 */
  pageSize: number
} 