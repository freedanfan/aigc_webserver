import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'
import config from './utils/config'

// 引入全局样式
import './assets/main.css'
import './assets/styles/cyberpunk-theme.css'

// 创建应用实例
const app = createApp(App)

// 注册全局插件
app.use(createPinia())
app.use(router)
app.use(Antd)

// 挂载应用
app.mount('#app')

// 输出环境信息
console.log(`应用名称: ${config.appTitle}`)
console.log(`应用版本: ${config.appVersion}`)
console.log(`当前环境: ${config.env}`)
console.log(`API 地址: ${config.apiBaseUrl}`)
console.log(`是否使用模拟数据: ${config.useMock}`)

// 开发环境下输出更多信息
if (config.isDev) {
  console.log('当前为开发环境，可以看到更多调试信息')
  console.log('环境变量:', import.meta.env)
} 