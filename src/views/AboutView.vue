<script setup lang="ts">
// 这里可以添加组件逻辑
</script>

<template>
  <div class="about">
    <h1>关于页面</h1>
    <p>这是一个使用 Vue 3 + TypeScript + Vite 构建的项目。</p>
    <p>项目特点：</p>
    <ul>
      <li>基于 Vue 3 的组合式 API</li>
      <li>TypeScript 支持</li>
      <li>Vite 构建工具</li>
      <li>Vue Router 路由管理</li>
      <li>Pinia 状态管理</li>
    </ul>
    <div class="back-link">
      <router-link to="/">返回首页</router-link>
    </div>
  </div>
</template>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  margin-bottom: 1.5rem;
  color: var(--color-heading);
}

p {
  margin-bottom: 1rem;
  line-height: 1.6;
}

ul {
  margin: 1rem 0 2rem 1.5rem;
  line-height: 1.6;
}

.back-link {
  margin-top: 2rem;
}

.back-link a {
  color: #646cff;
  text-decoration: none;
}

.back-link a:hover {
  text-decoration: underline;
}
</style> 