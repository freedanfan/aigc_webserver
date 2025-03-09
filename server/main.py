import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from source.routers import router as text2image_router

# 加载环境变量
load_dotenv()
LOCAL_SERVER_URL = os.getenv("LOCAL_SERVER_URL", "http://127.0.0.1:11002")

# 创建FastAPI应用
app = FastAPI(title="文本生成图像API", description="使用Together AI进行文本到图像的生成")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(text2image_router)

# 启动服务器
if __name__ == "__main__":
    # 从LOCAL_SERVER_URL解析主机和端口
    parts = LOCAL_SERVER_URL.split(":")
    host = parts[1].strip("/")
    port = int(parts[2]) if len(parts) > 2 else 11002
    
    uvicorn.run("main:app", host=host, port=port, reload=True)