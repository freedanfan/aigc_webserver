import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// https://vitejs.dev/config/
export default defineConfig({
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
      // 将所有请求转发到后端服务器
      '/api': {
        target: 'http://localhost:11002',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        // 添加错误处理，当后端不可用时不会阻止前端启动
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('代理请求错误:', err);
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
  }
}) 