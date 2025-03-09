import requests
import json
import os
from dotenv import load_dotenv
import sys
import time

# 添加项目根目录到 Python 路径，以便导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
load_dotenv()

# 获取服务器 URL
SERVER_URL = os.getenv("LOCAL_SERVER_URL", "http://127.0.0.1:11002")

def test_text2image():
    """
    测试文本生成图像接口
    """
    # 构建请求 URL
    url = f"{SERVER_URL}/image_generation"
    
    # 构建请求参数
    payload = {
        "prompt": "一只可爱的猫咪在草地上玩耍",
        "negativePrompt": "模糊, 变形, 低质量",
        "stylePrompt": "写实风格",
        "colorPrompt": "明亮色彩",
        "lightPrompt": "自然光照",
        "compositionPrompt": "居中构图",
        "count": 1
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

if __name__ == "__main__":
    test_text2image() 