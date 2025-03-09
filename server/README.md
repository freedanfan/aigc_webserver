# AIGC Web 服务器

这是一个使用 Together AI 进行文本到图像生成的 Web 服务。

## 项目结构

```
aigc_webserver/
├── main.py                # 主应用入口
├── requirements.txt       # 依赖管理文件
├── .env                   # 环境变量配置
├── source/                # 源代码目录
│   ├── algorithm.py       # 算法实现
│   ├── models.py          # 数据模型
│   └── routers.py         # API 路由
└── test_tools/            # 测试工具
    ├── README.md          # 测试工具说明
    ├── test_text2image.py # 基本测试脚本
    └── test_text2image_cli.py # 命令行测试工具
```

## 环境配置

### 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
# venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 安装依赖

克隆项目后，在项目根目录运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

### 环境变量配置

复制 `.env.example` 文件为 `.env`，并根据需要修改其中的配置：

```bash
cp .env.example .env
```

## 运行服务

启动服务器：

```bash
# 直接运行
python main.py

# 或使用 uvicorn（开发模式）
uvicorn main:app --reload --host 127.0.0.1 --port 11002
```

## API 文档

服务启动后，可以通过以下 URL 访问 API 文档：

- Swagger UI: http://127.0.0.1:11002/docs
- ReDoc: http://127.0.0.1:11002/redoc

## 测试工具

项目提供了测试工具，可以用来测试 API 接口：

```bash
# 运行基本测试
python test_tools/test_text2image.py

# 运行命令行测试工具
python test_tools/test_text2image_cli.py --prompt "一只可爱的猫咪在草地上玩耍" --negative_prompt "模糊, 变形, 低质量" --style_prompt "写实风格" --color_prompt "明亮色彩" --light_prompt "自然光照" --composition_prompt "居中构图" --count 1 --width 1024 --height 1024 --model "black-forest-labs/FLUX.1-schnell-Free" --need_optimize_prompt True
```

更多测试工具的使用说明，请参考 [test_tools/README.md](test_tools/README.md)。 