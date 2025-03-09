<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { DownOutlined, InboxOutlined, DeleteOutlined } from '@ant-design/icons-vue'
import type { UploadProps, UploadFile } from 'ant-design-vue'
import { imageApi } from '@/api'
import { GenerateImageParams, GeneratedImage } from '@/api/types'

const inputValue = ref('')
const negativePromptValue = ref('') // 反向提示词输入框的值
const loading = ref(false)
const useNegativePrompt = ref(false) // 是否使用反向提示词
const selectedOptions = ref<string[]>([]) // 选中的选项

// 上传图片相关状态
const fileList = ref<UploadFile[]>([])
const previewVisible = ref(false)
const previewImage = ref('')
const previewTitle = ref('')
const hasUploadedImage = ref(false) // 是否已上传图片
const imageBase64 = ref<string>('') // 存储图片的 base64 编码
const imageCount = ref<number>(1) // 生成图片数量，默认为 1，最大为 6

// 生成图片相关状态
const generatedImages = ref<GeneratedImage[]>([])
const isGenerating = ref<boolean>(false) // 是否正在生成图片

// 为每个选项创建独立的状态
const stylePrompt = ref<string>('no-style')
const colorPrompt = ref<string>('no-color')
const lightPrompt = ref<string>('no-light')
const compositionPrompt = ref<string>('no-composition')

// 选项列表配置
const promptOptions = {
  style: [
    { label: '无风格', value: 'no-style' },
    { label: '写实风格', value: 'realistic style' },
    { label: '动漫风格', value: 'anime style' },
    { label: '水彩风格', value: 'watercolor style' },
    { label: '油画风格', value: 'oil painting style' },
    { label: '素描风格', value: 'sketch style' },
    { label: '赛博朋克', value: 'cyberpunk style' },
    { label: '未来主义', value: 'futuristic style' },
    { label: '复古风格', value: 'vintage style' }
  ],
  color: [
    { label: '无色彩', value: 'no-color' },
    { label: '明亮色彩', value: 'bright colors' },
    { label: '柔和色调', value: 'soft colors' },
    { label: '暖色调', value: 'warm colors' },
    { label: '冷色调', value: 'cool colors' },
    { label: '黑白', value: 'black and white' },
    { label: '单色调', value: 'monochromatic' },
    { label: '高对比度', value: 'high contrast' }
  ],
  light: [
    { label: '无光照', value: 'no-light' },
    { label: '自然光', value: 'natural lighting' },
    { label: '柔和光', value: 'soft lighting' },
    { label: '逆光', value: 'backlight' },
    { label: '阳光', value: 'sunlight' },
    { label: '夜景', value: 'night scene' },
    { label: '聚光灯', value: 'spotlight' },
    { label: '环境光', value: 'ambient light' }
  ],
  composition: [
    { label: '无构图', value: 'no-composition' },
    { label: '对称构图', value: 'symmetrical composition' },
    { label: '黄金分割', value: 'golden ratio' },
    { label: '居中构图', value: 'centered composition' },
    { label: '三分法', value: 'rule of thirds' },
    { label: '对角线', value: 'diagonal composition' },
    { label: '框架构图', value: 'framing composition' },
    { label: '前景层次', value: 'foreground depth' }
  ]
}

/**
 * 将文件转换为 Base64
 * @param file 要转换的文件对象
 * @returns Promise，解析为 base64 字符串
 */
const getBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = error => reject(error)
  })
}

/**
 * 上传前检查文件
 * @param file 要上传的文件
 * @returns 是否允许上传
 */
const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    message.error('只能上传图片文件!')
  }
  const isLt20M = file.size / 1024 / 1024 < 20
  if (!isLt20M) {
    message.error('图片必须小于 20MB!')
  }
  return isImage && isLt20M
}

/**
 * 处理图片预览
 * @param file 要预览的文件
 */
const handlePreview = async (file: UploadFile) => {
  if (!file.url && !file.preview) {
    if (file.originFileObj) {
      file.preview = await getBase64(file.originFileObj)
    }
  }
  previewImage.value = file.url || file.preview || ''
  previewVisible.value = true
  previewTitle.value = file.name || file.url?.substring(file.url.lastIndexOf('/') + 1) || ''
}

/**
 * 处理图片上传状态变化
 * @param info 上传信息
 */
const handleChange: UploadProps['onChange'] = async ({ fileList: newFileList }) => {
  fileList.value = newFileList
  // 当有文件时，显示预览
  hasUploadedImage.value = newFileList.length > 0
  
  // 如果有新上传的文件，转换为 base64
  if (newFileList.length > 0 && newFileList[0].originFileObj) {
    try {
      // 获取并存储 base64 编码
      imageBase64.value = await getBase64(newFileList[0].originFileObj)
      
      // 设置预览图
      if (fileList.value.length > 0) {
        fileList.value[0].preview = imageBase64.value
      }
    } catch (error) {
      console.error('转换图片为 base64 失败:', error)
      message.error('图片处理失败，请重新上传')
    }
  } else {
    // 如果没有文件，清空 base64 编码
    imageBase64.value = ''
  }
}

/**
 * 删除图片
 */
const handleRemove = () => {
  fileList.value = []
  hasUploadedImage.value = false
  imageBase64.value = '' // 清空 base64 编码
}

/**
 * 生成图片
 * 将用户输入的提示词和上传的图片发送到后台
 */
const generateImage = async () => {
  // 验证输入，确保正向提示词已填写（必填项）
  if (!inputValue.value.trim()) {
    message.warning('请输入正向提示词')
    return
  }
  
  // 设置加载状态
  loading.value = true
  isGenerating.value = true
  
  try {
    // 准备请求参数，构建 API 所需的参数对象
    const params: GenerateImageParams = {
      // 用户输入的正向提示词（必填）
      prompt: inputValue.value,
      
      // 生成图片数量
      count: imageCount.value,
      
      // 仅当用户开启反向提示词时，才添加反向提示词
      negativePrompt: useNegativePrompt.value ? negativePromptValue.value : undefined,
      
      // 仅当用户选择了非默认风格时，才添加风格参数
      stylePrompt: stylePrompt.value !== 'no-style' ? stylePrompt.value : undefined,
      
      // 仅当用户选择了非默认色彩时，才添加色彩参数
      colorPrompt: colorPrompt.value !== 'no-color' ? colorPrompt.value : undefined,
      
      // 仅当用户选择了非默认光照时，才添加光照参数
      lightPrompt: lightPrompt.value !== 'no-light' ? lightPrompt.value : undefined,
      
      // 仅当用户选择了非默认构图时，才添加构图参数
      compositionPrompt: compositionPrompt.value !== 'no-composition' ? compositionPrompt.value : undefined
    }
    
    // 如果用户上传了参考图片，将其 base64 编码添加到参数中
    if (imageBase64.value) {
      params.referenceImage = imageBase64.value
    }
    
    // 调用 API 生成图片，等待响应
    // 注意：即使后端服务未启动，由于我们添加了模拟数据功能，这里仍然会正常工作
    const res = await imageApi.generateImage(params)
    
    // 处理响应结果
    if (res.data && res.data.length > 0) {
      // 更新生成的图片列表，显示在界面上
      generatedImages.value = res.data
      message.success(`成功生成 ${res.data.length} 张图片`)
    } else {
      // 如果返回的数据为空，提示用户调整参数
      message.warning('未能生成图片，请调整提示词后重试')
    }
  } catch (error) {
    // 捕获并处理请求过程中的错误
    console.error('生成图片失败:', error)
    message.error('图片生成失败，请稍后重试')
  } finally {
    // 无论成功还是失败，都需要重置状态
    loading.value = false  // 关闭加载状态
    isGenerating.value = false // 关闭生成状态
    inputValue.value = ''  // 清空输入框
  }
}

const handleSend = generateImage
</script>

<template>
  <a-layout class="layout">
    <!-- 头部 -->
    <a-layout-header class="header">
      <div class="header-content">
        <h1>AIGC webserver 的 AI 助手</h1>
        <p class="subtitle">基于 Vue 3 + TypeScript + Ant Design Vue 构建</p>
      </div>
    </a-layout-header>
    
    <!-- 内容区域 -->
    <a-layout-content class="content">
      <div class="content-wrapper">
        <!-- 左侧输入区域 -->
        <div class="chat-panel">
          <div class="chat-container">
            <div class="chat-messages">
              <div class="welcome-message">
                <h2>欢迎使用 AI 助手</h2>
                <p>请在下方输入框中输入您的问题，然后点击发送按钮或按回车键发送。</p>
              </div>
            </div>
            
            <div class="input-area">
              <div class="upload-container">
                <a-upload-dragger
                  v-show="!hasUploadedImage"
                  v-model:fileList="fileList"
                  name="file"
                  :multiple="false"
                  :before-upload="beforeUpload"
                  @preview="handlePreview"
                  @change="handleChange"
                  list-type="picture"
                  accept="image/*"
                  :showUploadList="false"
                >
                  <p class="ant-upload-drag-icon">
                    <inbox-outlined />
                  </p>
                  <p class="ant-upload-text">点击或拖拽图片到此区域上传</p>
                  <p class="ant-upload-hint">
                    支持单个图片上传，图片大小不超过20MB
                  </p>
                </a-upload-dragger>
                
                <div v-show="hasUploadedImage" class="image-preview-container">
                  <div class="image-preview" v-if="fileList.length > 0">
                    <img 
                      :src="fileList[0].url || fileList[0].preview || fileList[0].thumbUrl" 
                      :alt="fileList[0].name || '预览图片'" 
                      @click="handlePreview(fileList[0])"
                    />
                    <div class="image-actions">
                      <a-button 
                        type="primary" 
                        danger 
                        shape="circle" 
                        @click="handleRemove"
                        class="delete-button"
                      >
                        <template #icon><delete-outlined /></template>
                      </a-button>
                    </div>
                  </div>
                </div>
              </div>
              
              <a-textarea
                v-model:value="inputValue"
                placeholder="请输入正向提示词...(必填)"
                rows="4"
              />
              
              <a-textarea
                v-if="useNegativePrompt"
                v-model:value="negativePromptValue"
                placeholder="请输入反向提示词..."
                rows="4"
              />
              
              <div class="options-area">
                <a-switch 
                  v-model:checked="useNegativePrompt" 
                  :checked-children="'开启反向提示词'" 
                  :un-checked-children="'关闭反向提示词'"
                />
                
                <div class="image-count-container">
                  <span class="image-count-label">生成数量:</span>
                  <a-input-number
                    v-model:value="imageCount"
                    :min="1"
                    :max="6"
                    size="small"
                  />
                </div>
                
                <a-button type="primary" @click="generateImage" :loading="loading" class="send-button">
                  生成图片
                </a-button>
              </div>
              
              <div class="prompt-options">
                <a-select
                  v-model:value="stylePrompt"
                  placeholder="风格"
                  size="small"
                  :options="promptOptions.style"
                  show-search
                  allow-clear
                >
                  <template #suffixIcon><down-outlined /></template>
                </a-select>
                
                <a-select
                  v-model:value="colorPrompt"
                  placeholder="色彩"
                  size="small"
                  :options="promptOptions.color"
                  show-search
                  allow-clear
                >
                  <template #suffixIcon><down-outlined /></template>
                </a-select>
                
                <a-select
                  v-model:value="lightPrompt"
                  placeholder="光照"
                  size="small"
                  :options="promptOptions.light"
                  show-search
                  allow-clear
                >
                  <template #suffixIcon><down-outlined /></template>
                </a-select>
                
                <a-select
                  v-model:value="compositionPrompt"
                  placeholder="构图"
                  size="small"
                  :options="promptOptions.composition"
                  show-search
                  allow-clear
                >
                  <template #suffixIcon><down-outlined /></template>
                </a-select>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧结果展示区域 -->
        <div class="result-panel">
          <div class="result-container">
            <h2 class="result-title">生成结果</h2>
            <div v-if="isGenerating" class="loading-container">
              <a-spin tip="正在生成图片，请稍候..." />
            </div>
            <div v-else-if="generatedImages.length === 0" class="empty-result">
              <p>暂无生成结果，请点击"生成图片"按钮开始生成</p>
            </div>
            <div v-else class="result-gallery">
              <div v-for="image in generatedImages" :key="image.id" class="result-item">
                <a-image
                  :src="image.url"
                  :alt="image.title"
                  :title="image.title"
                  :preview="{
                    src: image.url,
                    mask: '预览'
                  }"
                />
                <div class="image-title">{{ image.title }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </a-layout-content>
    
    <!-- 底部 -->
    <a-layout-footer class="footer">
      AIGC Webserver ©2023 Created with Ant Design Vue
    </a-layout-footer>
    
    <!-- 图片预览 -->
    <a-modal
      :visible="previewVisible"
      :title="previewTitle"
      :footer="null"
      @cancel="previewVisible = false"
    >
      <img alt="预览图片" style="width: 100%" :src="previewImage" />
    </a-modal>
  </a-layout>
</template>

<style scoped>
/* 整体布局 */
.layout {
  padding-top: 250px;
  min-height: 100vh;
  background: transparent;
  display: flex;
  flex-direction: column;
  position: relative;
}

.layout::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:rgb(10,12,30);stop-opacity:1" /><stop offset="100%" style="stop-color:rgb(50,15,75);stop-opacity:1" /></linearGradient></defs><rect width="100%" height="100%" fill="url(%23grad)" /><g fill="none" stroke="rgba(45,170,220,0.1)" stroke-width="1"><path d="M0 50 L100 50 M50 0 L50 100" /><circle cx="50" cy="50" r="40" /><circle cx="50" cy="50" r="20" /><circle cx="50" cy="50" r="60" /></g><g fill="rgba(220,20,140,0.05)"><rect x="0" y="0" width="100" height="100" /><rect x="10" y="10" width="80" height="80" /><rect x="20" y="20" width="60" height="60" /></g></svg>');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.8;
  z-index: -1;
  pointer-events: none;
}

/* 头部样式 */
.header {
  background-color: rgba(20, 20, 35, 0.9);
  padding: 16px 0;
  height: auto;
  min-height: 80px;
  line-height: 1.5;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.header-content {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 16px;
  text-align: center;
}

.header h1 {
  color: #fff;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 8px;
  text-shadow: 0 0 15px rgba(0, 255, 255, 1), 0 0 25px rgba(0, 255, 255, 0.8);
  margin-top: auto;
}

.subtitle {
  color: rgba(255, 255, 255, 0.85);
  font-size: 1rem;
  margin: 0;
  text-shadow: 0 0 8px rgba(255, 0, 255, 0.8);
}

/* 内容区域 */
.content {
  padding: 24px;
  flex: 1;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 1;
  overflow-y: auto;
}

.content-wrapper {
  max-width: 2400px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  gap: 24px;
  position: relative;
  height: 100%;
  justify-content: center; /* 水平居中 */
}

/* 左右面板 */
.chat-panel, .result-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 575px;
}

/* 聊天容器样式 */
.chat-container {
  background-color: rgba(20, 20, 35, 0.85);
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3), 0 0 40px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  border: 1px solid rgba(0, 255, 255, 0.2);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 0 0 auto;
  padding: 16px;
}

.welcome-message {
  text-align: center;
  padding: 16px;
  background-color: rgba(30, 30, 50, 0.7);
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #fff;
}

.welcome-message h2 {
  margin-bottom: 8px;
  color: #0ff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
  font-size: 1.5rem;
  font-weight: bold;
}

.welcome-message p {
  color: rgba(255, 255, 255, 0.85);
  font-size: 1rem;
  line-height: 1.5;
}

/* 结果容器样式 */
.result-container {
  background-color: rgba(20, 20, 35, 0.85);
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3), 0 0 40px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  border: 1px solid rgba(0, 255, 255, 0.2);
  padding: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.result-title {
  color: #0ff;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 16px;
  text-align: center;
}

.result-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  overflow-y: auto;
  flex: 1;
}

.result-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px;
  background-color: rgba(30, 30, 50, 0.5);
  border-radius: 4px;
  border: 1px solid rgba(0, 255, 255, 0.2);
  transition: all 0.3s;
}

.result-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
  border-color: rgba(0, 255, 255, 0.5);
}

.image-title {
  color: #fff;
  margin-top: 8px;
  font-size: 0.9rem;
  text-align: center;
}

:deep(.ant-image) {
  width: 100%;
  height: 140px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid rgba(0, 255, 255, 0.3);
  transition: all 0.3s;
}

:deep(.ant-image-img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 输入区域样式 */
.input-area {
  padding: 16px;
  border-top: 1px solid rgba(0, 255, 255, 0.3);
  background-color: rgba(20, 20, 35, 0.9);
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex: 1;
}

/* 上传容器样式 */
.upload-container {
  width: 100%;
}

.image-preview-container {
  width: 100%;
  padding: 16px;
  background-color: rgba(30, 30, 50, 0.7);
  border: 1px dashed rgba(0, 255, 255, 0.4);
  border-radius: 2px;
  text-align: center;
}

.image-preview {
  position: relative;
  display: inline-block;
  max-width: 100%;
}

.image-preview img {
  max-width: 100%;
  max-height: 200px;
  cursor: pointer;
  border: 1px solid rgba(255, 0, 255, 0.3);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
}

.image-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 8px;
}

.delete-button {
  opacity: 0.8;
  box-shadow: 0 0 10px rgba(255, 0, 100, 0.4);
}

.delete-button:hover {
  opacity: 1;
  box-shadow: 0 0 15px rgba(255, 0, 100, 0.6);
}

/* 选项区域样式 */
.options-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.image-count-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.image-count-label {
  color: #fff;
  font-size: 0.9rem;
}

.send-button {
  background: linear-gradient(45deg, #0ff, #f0f);
  border: none;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  font-weight: bold;
  font-size: 1rem;
  height: auto;
  padding: 8px 16px;
}

.send-button:hover {
  background: linear-gradient(45deg, #0ff, #f0f);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
  opacity: 0.9;
}

.prompt-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.prompt-options :deep(.ant-select) {
  width: 100%;
}

/* Ant Design 组件样式覆盖 */
:deep(.ant-upload-list) {
  display: none;
}

:deep(.ant-select-selector) {
  background-color: rgba(30, 30, 50, 0.8) !important;
  border: 1px solid rgba(0, 255, 255, 0.5) !important;
  color: #fff !important;
}

:deep(.ant-select-selection-placeholder) {
  color: rgba(255, 255, 255, 0.8) !important;
}

:deep(.ant-select-selection-item) {
  color: #0ff !important;
  font-weight: bold;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}

:deep(.ant-textarea) {
  background-color: rgba(30, 30, 50, 0.7);
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #fff;
  font-size: 1rem;
}

:deep(.ant-textarea::placeholder) {
  color: rgba(255, 255, 255, 0.7);
}

:deep(.ant-textarea:focus) {
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  border-color: rgba(0, 255, 255, 0.7);
}

:deep(.ant-upload-drag) {
  background-color: rgba(30, 30, 50, 0.8);
  border: 1px dashed rgba(0, 255, 255, 0.5);
  transition: all 0.3s;
}

:deep(.ant-upload-drag:hover) {
  border-color: rgba(0, 255, 255, 0.9);
  background-color: rgba(40, 40, 70, 0.8);
}

:deep(.ant-upload-drag-icon) {
  color: #0ff;
  font-size: 2.5rem;
  margin-bottom: 8px;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
}

:deep(.ant-upload-text) {
  color: #fff !important;
  font-size: 1.1rem;
  font-weight: bold;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

:deep(.ant-upload-hint) {
  color: rgba(255, 255, 255, 0.8) !important;
  font-size: 0.9rem;
}

/* 底部样式 */
.footer {
  text-align: center;
  background-color: rgba(20, 20, 35, 0.9);
  color: rgba(255, 255, 255, 0.65);
  padding: 16px;
  position: relative;
  z-index: 10;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  margin-top: auto;
}

/* 响应式布局 */
@media (max-width: 992px) {
  .content-wrapper {
    flex-direction: column;
    height: auto;
  }
  
  .chat-panel, .result-panel {
    width: 100%;
    height: auto;
  }
  
  .result-panel {
    margin-top: 24px;
  }
  
  .header-content {
    padding: 0 12px;
  }
  
  .header h1 {
    font-size: 1.8rem;
  }
}

@media (max-width: 576px) {
  .prompt-options {
    grid-template-columns: 1fr;
  }
  
  .header h1 {
    font-size: 1.5rem;
    margin-bottom: 4px;
  }
  
  .subtitle {
    font-size: 0.9rem;
  }
  
  .content {
    padding: 16px 8px;
  }
  
  .header {
    min-height: 70px;
    padding: 8px 0;
  }
  
  .header-content {
    padding: 0 8px;
  }
}

/* 添加新样式 */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.empty-result {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: rgba(255, 255, 255, 0.65);
  font-size: 1rem;
  text-align: center;
}
</style> 