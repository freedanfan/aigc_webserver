import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd())
  
  // 获取环境变量，如果不存在则使用默认值
  const apiBaseUrl = env.VITE_APP_API_BASE_URL || 'http://localhost:11002'
  const apiPrefix = env.VITE_APP_API_PREFIX || '/api'
  
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },
    server: {
      port: 3000,
      open: true,
      cors: true,
      proxy: {
        // 将 API 请求转发到后端服务器
        [apiPrefix]: {
          target: apiBaseUrl,
          changeOrigin: true,
          rewrite: (path) => path.replace(new RegExp(`^${apiPrefix}`), ''),
          secure: false, // 如果是 https 且有证书问题，设置为 false
          // 添加错误处理，当后端不可用时不会阻止前端启动
          configure: (proxy, options) => {
            proxy.on('error', (err, req, res) => {
              console.log(`代理请求错误 [${mode}]:`, err);
              // 返回一个友好的错误响应，而不是中断请求
              res.writeHead(500, {
                'Content-Type': 'application/json',
              });
              res.end(JSON.stringify({ 
                code: 500, 
                message: '后端服务不可用，使用模拟数据',
                data: null
              }));
            });
          }
        }
      }
    },
    build: {
      // 生产环境构建配置
      outDir: 'dist', // 输出目录
      assetsDir: 'assets', // 静态资源目录
      sourcemap: false, // 生产环境不需要 sourcemap
      minify: 'terser', // 使用 terser 进行压缩
      terserOptions: {
        compress: {
          drop_console: env.VITE_APP_ENV === 'production', // 生产环境删除 console
          drop_debugger: env.VITE_APP_ENV === 'production', // 生产环境删除 debugger
        },
      },
      // 分块策略
      rollupOptions: {
        output: {
          chunkFileNames: 'assets/js/[name]-[hash].js',
          entryFileNames: 'assets/js/[name]-[hash].js',
          assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
          manualChunks: {
            vue: ['vue', 'vue-router', 'pinia'],
            'ant-design-vue': ['ant-design-vue'],
          },
        },
      },
    },
    // 基本公共路径，如果部署在子路径下需要修改
    base: '/',
  }
}) 