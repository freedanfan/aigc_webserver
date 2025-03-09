# 测试工具

本目录包含用于测试 API 接口的工具脚本。

## 文本生成图像测试工具

### 基本测试脚本

`test_text2image.py` 是一个简单的测试脚本，用于测试文本生成图像接口。

使用方法：

```bash
python test_tools/test_text2image.py
```

这个脚本会使用默认参数向服务器发送请求，生成一张猫咪图像。

### 命令行测试工具

`test_text2image_cli.py` 是一个更灵活的命令行工具，支持自定义参数。

使用方法：

```bash
python test_tools/test_text2image_cli.py --prompt "一只可爱的猫咪在草地上玩耍" --steps 4 --width 1024 --height 1024 --model "black-forest-labs/FLUX.1-schnell-Free" --n 1
```

参数说明：

- `--prompt`: 生成图像的文本提示词
- `--steps`: 生成步数
- `--width`: 输出图像宽度
- `--height`: 输出图像高度
- `--model`: 使用的模型名称
- `--n`: 生成图像的数量

所有参数都有默认值，可以根据需要选择性地指定。

## 注意事项

1. 确保服务器已经启动
2. 确保环境变量已正确配置（可以通过 `.env` 文件或系统环境变量）
3. 请求可能需要一些时间来处理，特别是当生成步数较多或图像尺寸较大时 