<script setup lang="ts">
import { ref } from 'vue'
import { message } from 'ant-design-vue'

const inputValue = ref('')
const loading = ref(false)

const handleSend = () => {
  if (!inputValue.value.trim()) {
    message.warning('请输入内容')
    return
  }
  
  loading.value = true
  
  // 模拟发送请求
  setTimeout(() => {
    message.success('发送成功：' + inputValue.value)
    inputValue.value = ''
    loading.value = false
  }, 1000)
}
</script>

<template>
  <div class="home-container">
    <div class="header">
      <h1>AIGC webserver 的 AI 助手</h1>
      <p class="subtitle">基于 Vue 3 + TypeScript + Ant Design Vue 构建</p>
    </div>
    
    <div class="chat-container">
      <div class="chat-messages">
        <div class="welcome-message">
          <h2>欢迎使用 AI 助手</h2>
          <p>请在下方输入框中输入您的问题，然后点击发送按钮或按回车键发送。</p>
        </div>
      </div>
      
      <div class="input-area">
        <a-input-search
          v-model:value="inputValue"
          placeholder="请输入您的问题..."
          size="large"
          :loading="loading"
          @search="handleSend"
          enter-button="发送"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  min-height: 80vh;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.subtitle {
  color: var(--color-text-light);
  margin-top: 0.5rem;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  min-height: 300px;
}

.welcome-message {
  text-align: center;
  padding: 2rem;
  background-color: rgba(240, 240, 240, 0.5);
  border-radius: 8px;
}

.welcome-message h2 {
  margin-bottom: 1rem;
  color: var(--color-heading);
}

.input-area {
  padding: 1rem;
  border-top: 1px solid #eee;
  background-color: white;
}

@media (prefers-color-scheme: dark) {
  .chat-container {
    background-color: rgba(30, 30, 30, 0.8);
  }
  
  .welcome-message {
    background-color: rgba(50, 50, 50, 0.5);
  }
  
  .input-area {
    background-color: #1a1a1a;
    border-top: 1px solid #333;
  }
}
</style> 