<script setup lang="ts">
defineProps<{
  msg: string
}>()
</script>

<template>
  <div class="greetings">
    <h1 class="title">{{ msg }}</h1>
    <h3>
      欢迎使用 Vue 3 + TypeScript + Vite 构建的项目
    </h3>
    <p>
      这是一个使用 Vue 3 的 <code>script setup</code> 语法和 TypeScript 构建的项目。
    </p>
  </div>
</template>

<style scoped>
.greetings {
  text-align: center;
  margin-bottom: 2rem;
}

h1 {
  font-weight: 700;
  font-size: 2.6rem;
  position: relative;
  margin-bottom: 1rem;
  color: var(--color-heading);
}

h3 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: var(--color-text);
}

p {
  color: var(--color-text-light);
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: center;
  }
}
</style> 