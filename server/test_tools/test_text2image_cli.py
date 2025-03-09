import requests
import json
import os
import argparse
from dotenv import load_dotenv
import sys
import time

# 添加项目根目录到 Python 路径，以便导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
load_dotenv()

# 获取服务器 URL
SERVER_URL = os.getenv("LOCAL_SERVER_URL", "http://127.0.0.1:11002")

def test_text2image(prompt, negative_prompt="模糊, 变形, 低质量", style_prompt="写实风格", 
                   color_prompt="明亮色彩", light_prompt="自然光照", 
                   composition_prompt="居中构图", count=1, model=None, 
                   width=None, height=None, need_optimize_prompt=True):
    """
    测试文本生成图像接口
    
    参数:
        prompt (str): 生成图像的文本提示词
        negative_prompt (str): 负面提示词，指定不希望出现在图像中的内容
        style_prompt (str): 风格提示词，指定图像的艺术风格
        color_prompt (str): 颜色提示词，指定图像的色彩偏好
        light_prompt (str): 光照提示词，指定图像的光照效果
        composition_prompt (str): 构图提示词，指定图像的构图方式
        count (int): 生成图像的数量
        model (str): 使用的模型名称
        width (int): 输出图像宽度
        height (int): 输出图像高度
        need_optimize_prompt (bool): 是否需要优化提示词
    """
    # 构建请求 URL
    url = f"{SERVER_URL}/image_generation"
    
    # 构建请求参数
    payload = {
        "prompt": prompt,
        "negativePrompt": negative_prompt,
        "stylePrompt": style_prompt,
        "colorPrompt": color_prompt,
        "lightPrompt": light_prompt,
        "compositionPrompt": composition_prompt,
        "count": count,
        "needOptimizePrompt": need_optimize_prompt
    }
    
    # 添加可选参数
    if model:
        payload["model"] = model
    if width:
        payload["width"] = width
    if height:
        payload["height"] = height
    
    # 打印请求信息
    print(f"发送请求到: {url}")
    print(f"请求参数: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 发送 POST 请求
        response = requests.post(url, json=payload)
        
        # 记录结束时间
        end_time = time.time()
        
        # 计算请求耗时
        elapsed_time = end_time - start_time
        
        # 打印响应状态码和耗时
        print(f"响应状态码: {response.status_code}")
        print(f"请求耗时: {elapsed_time:.2f} 秒")
        
        # 如果响应成功，打印响应内容
        if response.status_code == 200:
            response_data = response.json()
            print(f"响应内容: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
            
            # 检查生成的图像信息
            if response_data.get("data") and len(response_data["data"]) > 0:
                print(f"成功生成 {len(response_data['data'])} 张图像")
                for i, image_info in enumerate(response_data["data"]):
                    print(f"图像 {i+1} ID: {image_info.get('id')}")
                    print(f"图像 {i+1} 标题: {image_info.get('title')}")
                    print(f"图像 {i+1} URL: {image_info.get('url')}")
                    print(f"图像 {i+1} 创建时间: {image_info.get('createdAt')}")
            else:
                print("未生成任何图像")
        else:
            print(f"请求失败: {response.text}")
    
    except Exception as e:
        print(f"发生错误: {str(e)}")

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="测试文本生成图像API")
    
    # 添加命令行参数
    parser.add_argument("--prompt", type=str, default="一只可爱的猫咪在草地上玩耍", help="生成图像的文本提示词")
    parser.add_argument("--negative_prompt", type=str, default="模糊, 变形, 低质量", help="负面提示词，指定不希望出现在图像中的内容")
    parser.add_argument("--style_prompt", type=str, default="写实风格", help="风格提示词，指定图像的艺术风格")
    parser.add_argument("--color_prompt", type=str, default="明亮色彩", help="颜色提示词，指定图像的色彩偏好")
    parser.add_argument("--light_prompt", type=str, default="自然光照", help="光照提示词，指定图像的光照效果")
    parser.add_argument("--composition_prompt", type=str, default="居中构图", help="构图提示词，指定图像的构图方式")
    parser.add_argument("--count", type=int, default=1, help="生成图像的数量")
    parser.add_argument("--model", type=str, help="使用的模型名称")
    parser.add_argument("--width", type=int, help="输出图像宽度")
    parser.add_argument("--height", type=int, help="输出图像高度")
    parser.add_argument("--need_optimize_prompt", type=bool, default=True, help="是否需要优化提示词，接受 True 或 False")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用测试函数
    test_text2image(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        style_prompt=args.style_prompt,
        color_prompt=args.color_prompt,
        light_prompt=args.light_prompt,
        composition_prompt=args.composition_prompt,
        count=args.count,
        model=args.model,
        width=args.width,
        height=args.height,
        need_optimize_prompt=args.need_optimize_prompt
    )

if __name__ == "__main__":
    main() 