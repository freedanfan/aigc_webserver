# AIGC Webserver - AI 图像生成助手

基于 Vue 3 + TypeScript + Ant Design Vue 构建的 AI 图像生成助手，具有赛博朋克风格的用户界面。

## 项目特点

- 🚀 **现代化前端框架** - 使用 Vue 3 的组合式 API 和 TypeScript
- 🎨 **赛博朋克风格界面** - 独特的视觉设计，霓虹色彩和未来感
- 📷 **图片上传与预览** - 支持拖拽上传和预览图片
- 🔤 **提示词系统** - 支持正向和反向提示词输入
- 🎭 **风格选择器** - 内置多种风格、色彩、光照和构图选项
- 📱 **响应式设计** - 适配不同设备尺寸
- 🌓 **深色模式支持** - 自动适应系统深色模式

## 技术栈

- [Vue 3](https://v3.cn.vuejs.org/) - 渐进式 JavaScript 框架
- [TypeScript](https://www.typescriptlang.org/) - JavaScript 的超集，提供类型检查
- [Vite](https://cn.vitejs.dev/) - 下一代前端构建工具
- [Ant Design Vue](https://antdv.com/) - 企业级 UI 组件库
- [Vue Router](https://router.vuejs.org/zh/) - Vue.js 官方路由管理器
- [Pinia](https://pinia.vuejs.org/zh/) - Vue 的状态管理库

## 项目结构

```
aigc_webserver/
├── public/                 # 静态资源
├── src/                    # 源代码
│   ├── assets/             # 资源文件
│   │   ├── main.css        # 基础样式
│   │   └── styles/         # 样式文件夹
│   │       └── cyberpunk-theme.css  # 赛博朋克主题样式
│   ├── components/         # 组件
│   ├── router/             # 路由
│   ├── views/              # 页面
│   │   ├── HomeView.vue    # 主页 - 图像生成界面
│   │   └── AboutView.vue   # 关于页面
│   ├── App.vue             # 根组件
│   └── main.ts             # 入口文件
├── package.json            # 项目依赖
└── README.md               # 项目说明
```

## 功能说明

### 图片上传

- 支持拖拽或点击上传图片
- 支持图片预览和删除
- 限制图片大小为 20MB
- 仅支持图片格式文件

### 提示词系统

- 正向提示词：描述你想要生成的图像内容
- 反向提示词：描述你不希望出现在图像中的内容
- 可通过开关控制反向提示词的显示/隐藏

### 风格选择器

项目内置四种类型的选择器，帮助用户快速选择图像风格：

1. **风格选择器**：写实风格、动漫风格、水彩风格等
2. **色彩选择器**：明亮色彩、柔和色调、暖色调等
3. **光照选择器**：自然光、柔和光、逆光等
4. **构图选择器**：对称构图、黄金分割、居中构图等

## 样式组织

项目采用了组件化的样式组织方式：

1. **组件样式**：
   - 使用 Vue 的 `<style scoped>` 块
   - 使用 `:deep()` 选择器处理组件内部样式

2. **主题样式**：
   - 赛博朋克风格的界面设计
   - 霓虹色彩和发光效果
   - 深色背景和半透明元素

## 开发指南

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 代码检查

```bash
npm run lint
```

## 未来计划

- [ ] 添加更多风格选项
- [ ] 实现图像生成 API 集成
- [ ] 添加历史记录功能
- [ ] 支持图像编辑和调整
- [ ] 添加用户认证系统

## 贡献指南

欢迎贡献代码、报告问题或提出新功能建议。请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 推荐的 IDE 设置

- [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar)

## 自定义配置

查看 [Vite 配置参考](https://cn.vitejs.dev/config/)。

# Vue 和 TypeScript 实现网站页面

## 项目设置

首先，我们需要创建一个基于 Vue 3 和 TypeScript 的项目。可以使用 Vue CLI 或 Vite 来快速搭建项目。

使用 Vite 创建项目：
