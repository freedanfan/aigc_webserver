import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 引入 Ant Design Vue
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

// 引入全局样式
import './assets/main.css'
import './assets/styles/cyberpunk-theme.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd) // 使用 Ant Design Vue

app.mount('#app') 