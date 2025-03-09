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
    }
  }
}) 