<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import { DownOutlined, InboxOutlined, DeleteOutlined } from '@ant-design/icons-vue'
import type { UploadProps, UploadFile } from 'ant-design-vue'

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

// 生成图片相关状态
const generatedImages = ref([
  { id: 1, url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png', title: '生成图片 1' },
  { id: 2, url: 'https://gw.alipayobjects.com/zos/antfincdn/LlvErxo8H9/photo-1503185912284-5271ff81b9a8.webp', title: '生成图片 2' },
  { id: 3, url: 'https://gw.alipayobjects.com/zos/antfincdn/cV16ZqzMjW/photo-1473091540282-9b846e7965e3.webp', title: '生成图片 3' },
  { id: 4, url: 'https://gw.alipayobjects.com/zos/antfincdn/x43I27A55%26/photo-1438109491414-7198515b166b.webp', title: '生成图片 4' },
])

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

// 上传前检查文件
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

// 处理图片预览
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

// 处理图片上传状态变化
const handleChange: UploadProps['onChange'] = ({ fileList: newFileList }) => {
  fileList.value = newFileList
  // 当有文件时，显示预览
  hasUploadedImage.value = newFileList.length > 0
  
  // 如果有新上传的文件，尝试生成预览
  if (newFileList.length > 0 && newFileList[0].originFileObj && !newFileList[0].preview) {
    getBase64(newFileList[0].originFileObj).then(url => {
      if (fileList.value.length > 0) {
        fileList.value[0].preview = url
      }
    })
  }
}

// 删除图片
const handleRemove = () => {
  fileList.value = []
  hasUploadedImage.value = false
}

// 将文件转换为 Base64
const getBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = error => reject(error)
  })
}

// 模拟生成图片
const generateImage = () => {
  if (!inputValue.value.trim() && fileList.value.length === 0) {
    message.warning('请输入内容或上传图片')
    return
  }
  
  loading.value = true
  
  // 模拟发送请求
  setTimeout(() => {
    message.success('图片生成成功')
    inputValue.value = ''
    loading.value = false
  }, 1000)
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
                placeholder="请输入正向提示词..."
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
            <div class="result-gallery">
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
</style> 