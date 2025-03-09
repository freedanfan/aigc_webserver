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

def test_text2image(prompt, generate_steps=4, width=1024, height=1024, model="black-forest-labs/FLUX.1-schnell-Free", n=1):
    """
    测试文本生成图像接口
    
    参数:
        prompt (str): 生成图像的文本提示词
        generate_steps (int): 生成步数
        width (int): 输出图像宽度
        height (int): 输出图像高度
        model (str): 使用的模型名称
        n (int): 生成图像的数量
    """
    # 构建请求 URL
    url = f"{SERVER_URL}/text2image"
    
    # 构建请求参数
    payload = {
        "prompt": prompt,
        "generate_steps": generate_steps,
        "output_size_width": width,
        "output_size_height": height,
        "model": model,
        "n": n
    }
    
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
            
            # 检查生成的图像 URL
            if response_data.get("data") and len(response_data["data"]) > 0:
                print(f"成功生成 {len(response_data['data'])} 张图像")
                for i, image_url in enumerate(response_data["data"]):
                    print(f"图像 {i+1} URL: {image_url}")
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
    parser.add_argument("--steps", type=int, default=4, help="生成步数")
    parser.add_argument("--width", type=int, default=1024, help="输出图像宽度")
    parser.add_argument("--height", type=int, default=1024, help="输出图像高度")
    parser.add_argument("--model", type=str, default="black-forest-labs/FLUX.1-schnell-Free", help="使用的模型名称")
    parser.add_argument("--n", type=int, default=1, help="生成图像的数量")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用测试函数
    test_text2image(
        prompt=args.prompt,
        generate_steps=args.steps,
        width=args.width,
        height=args.height,
        model=args.model,
        n=args.n
    )

if __name__ == "__main__":
    main() 