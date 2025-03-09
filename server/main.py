import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
from source.routers import router as text2image_router

# 加载环境变量
load_dotenv()
LOCAL_SERVER_URL = os.getenv("LOCAL_SERVER_URL", "http://127.0.0.1:11002")

# 创建FastAPI应用
app = FastAPI(
    title="AIGC 图像生成 API",
    description="""
    使用 Together AI 进行文本到图像的生成。
    
    ## 功能特点
    
    * 支持文本到图像生成
    * 支持多种提示词组合
    * 支持自定义图像尺寸
    * 支持多种模型选择
    
    ## 使用说明
    
    1. 选择合适的 API 端点
    2. 填写必要的参数
    3. 发送请求并获取生成的图像
    """,
    version="1.0.0",
    docs_url=None,  # 禁用默认的 docs 路径，我们将自定义它
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

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

# 自定义 OpenAPI 文档
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # 添加示例请求体到 OpenAPI 模式
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    if "examples" not in openapi_schema["components"]:
        openapi_schema["components"]["examples"] = {}
    
    # 添加图像生成请求示例
    openapi_schema["components"]["examples"]["ImageGenerationRequest"] = {
        "summary": "图像生成请求示例",
        "description": "一个完整的图像生成请求示例，包含所有可用参数",
        "value": {
            "prompt": "一只可爱的猫咪在草地上玩耍",
            "negativePrompt": "模糊, 变形, 低质量",
            "stylePrompt": "写实风格",
            "colorPrompt": "明亮色彩",
            "lightPrompt": "自然光照",
            "compositionPrompt": "居中构图",
            "count": 1,
            "width": 1024,
            "height": 1024,
            "model": "black-forest-labs/FLUX.1-schnell-Free",
            "needOptimizePrompt": True
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 自定义 Swagger UI 路径
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_favicon_url="/favicon.ico",
    )

# 启动服务器
if __name__ == "__main__":
    # 从LOCAL_SERVER_URL解析主机和端口
    parts = LOCAL_SERVER_URL.split(":")
    host = parts[1].strip("/")
    port = int(parts[2]) if len(parts) > 2 else 11002
    
    uvicorn.run("main:app", host=host, port=port, reload=True)