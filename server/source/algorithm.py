import os
import base64
import io
import boto3
import uuid
import logging
from dotenv import load_dotenv
from together import Together


class ImageGenerator:
    def __init__(self):
        # 加载配置参数文件
        load_dotenv()
        # 检查必要的环境变量是否存在
        self._check_environment_variables()
        self.api_key = os.getenv("TOGETHER_API_KEY")
        self.model = os.getenv("TOGETHER_MODEL")
        self.togetherai_client = Together(api_key=self.api_key)
        self.s3_client = self._init_s3_client()

        self.max_image_count = int(os.getenv("MAX_IMAGE_COUNT", 6))

    def _check_environment_variables(self):
        required_env_vars = [
            "S3_ENDPOINT_URL", 
            "S3_ACCESS_KEY_ID",
            "S3_SECRET_ACCESS_KEY", 
            "S3_BUCKET_NAME",
            "TOGETHER_MODEL",
            "TOGETHER_API_KEY"
        ]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"缺少必要的环境变量: {','.join(missing_vars)}")

    def _init_s3_client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
            endpoint_url=os.getenv("S3_ENDPOINT_URL")
        )

    def _get_steps(self, model):
        if "FLUX.1-schnell" in model:    # 免费的step最高为4
            return 4
        else:
            return 12

    def _upload_to_s3(self, image_data, folder_name):
        # 为图片生成唯一的文件名
        image_name = f"{folder_name}/{uuid.uuid4()}.png"
        
        # 直接上传到S3，不需要存储到本地
        self.s3_client.put_object(
            Bucket=os.getenv("S3_BUCKET_NAME"),
            Key=image_name,
            Body=io.BytesIO(image_data),
            ACL='public-read',
            ContentType='image/png'
        )
        
        # 生成URL并返回
        s3_url = f"{os.getenv('S3_ENDPOINT_URL')}/{os.getenv('S3_BUCKET_NAME')}/{image_name}"
        return s3_url

    async def text2image(self, 
                        prompt: str, 
                        generate_steps: int = None,
                        model: str = None,
                        output_size_width: int = 1024, 
                        output_size_height: int = 1024, 
                        n: int = 1,
                        need_optimize_prompt: bool = False):
        
        if not model:
            model = self.model  

        if generate_steps:
            steps = generate_steps
        else:
            steps = self._get_steps(model)

        if need_optimize_prompt:
            prompt = self.optimize_prompt(prompt)
        # 创建一个列表来存储所有生成的图片URL
        s3_urls = []

        if n > self.max_image_count:   
            n = self.max_image_count
            print(f"您生成的图片数量超过最大限制，已自动调整为最大限制: {n}")
        # 循环生成n张图片
        for _ in range(n):
            response = self.togetherai_client.images.generate(
                prompt=f"[{prompt}]",
                model=model,
                width=output_size_width,
                height=output_size_height,
                steps=steps,
                n=1,
                response_format="b64_json"
            )
            
            # 处理生成的图片
            for i in range(len(response.data)):
                # 将base64字符串解码为图片数据
                image_data = base64.b64decode(response.data[i].b64_json)
                
                # 上传到S3并获取URL
                s3_url = self._upload_to_s3(image_data, "output_text2image")
                print(f"图片已上传到S3，URL为：{s3_url}")
                s3_urls.append(s3_url)
        # 返回包含所有URL的列表
        return s3_urls

    async def image2image(self,
                        image_url: str,
                        prompt: str = "",
                        generate_steps: int = 4,
                        output_size_width: int = 1024,
                        output_size_height: int = 1024,
                        model: str = "black-forest-labs/FLUX.1-schnell-Free",
                        n: int = 1,
                        strength: float = 0.8,
                        need_optimize_prompt: bool = False):
        """
        使用Together AI的API进行图生图转换
        
        参数:
            image_url (str): 输入图像的URL
            prompt (str): 描述目标图像的文本提示词
            generate_steps (int): 生成步数
            output_size_width (int): 输出图像宽度
            output_size_height (int): 输出图像高度
            model (str): 使用的模型名称
            n (int): 生成图像的数量
            strength (float): 转换强度，值在0-1之间，越高表示对原图的改变越大
            need_optimize_prompt (bool): 是否需要优化提示词
            
        返回:
            list: 生成图像的S3 URL列表
        """
        import requests
        
        # 设置steps的数值
        steps = self._get_steps(model)
        
        # 如果需要优化提示词
        if need_optimize_prompt and prompt:
            prompt = self.optimize_prompt(prompt)
        
        # 下载输入图像
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            raise Exception(f"无法下载输入图像: {image_response.status_code}")
        
        # 将图像转换为base64编码
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')
        
        # 调用Together AI的图生图API
        response = self.togetherai_client.images.edit(
            image=image_base64,
            prompt=f"[{prompt}]" if prompt else "",
            model=model,
            width=output_size_width,
            height=output_size_height,
            steps=generate_steps,
            n=n,
            strength=strength,
            response_format="b64_json"
        )
        
        # 创建一个列表来存储所有生成的图片URL
        s3_urls = []
        
        # 处理每个生成的图片
        for i in range(len(response.data)):
            # 将base64字符串解码为图片数据
            image_data = base64.b64decode(response.data[i].b64_json)
            
            # 上传到S3并获取URL
            s3_url = self._upload_to_s3(image_data, "output_image2image")
            print(f"图生图结果已上传到S3，URL为：{s3_url}")
            s3_urls.append(s3_url)
        
        # 返回包含所有URL的列表
        return s3_urls

    def optimize_prompt(self, prompt, max_retries=5):
        """
        使用Azure OpenAI API优化提示词，将任何语言的提示词转换为英文格式
        
        参数:
            prompt (str): 用户输入的原始提示词
            max_retries (int): 最大重试次数
            
        返回:
            str: 优化后的英文提示词
        """
        import requests
        import json
        import logging
        
        # 获取Azure OpenAI API配置
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_base = os.getenv("AZURE_OPENAI_API_BASE")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        model = os.getenv("AZURE_OPENAI_MODEL")
        
        # 构建API请求URL
        url = f"{api_base}/openai/deployments/{model}/chat/completions?api-version={api_version}"
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        
        # 构建请求体
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的提示词优化助手，专门为FLUX图像生成模型优化提示词。你的任务是将用户输入的任何语言的提示词转换为高质量、详细的英文提示词。请添加丰富的视觉细节，包括光照效果、材质描述、视角、风格、色彩方案等。使用FLUX模型喜欢的关键词和格式，如'highly detailed'、'4k resolution'、'masterpiece'等增强词。确保最终提示词既保留原始意图，又能最大化FLUX模型的生成效果。请直接返回纯文本格式的提示词，不要包含任何JSON结构、大括号{}、中括号[]、反引号`，也不要在回复中包含'prompt'这个词。"
                },
                {
                    "role": "user",
                    "content": f"请将以下提示词转换为高质量的英文提示词，用于FLUX AI图像生成模型。添加必要的视觉细节、风格描述和技术参数，但保持原始概念不变。直接返回纯文本格式的提示词，不要包含任何JSON结构或标记：\n\n{prompt}"
                }
            ],
            "temperature": 0.8,
            "max_tokens": 500,
            "top_p": 0.95,
            "response_format": { "type": "text" }
        }
        
        retry_count = 0
        while retry_count < max_retries:
            try:
                # 发送请求
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()  # 如果请求失败，抛出异常
                
                # 解析响应
                result = response.json()
                optimized_prompt = result["choices"][0]["message"]["content"].strip()
                
                # 验证返回的提示词格式
                if '{' in optimized_prompt or '}' in optimized_prompt or '[' in optimized_prompt or ']' in optimized_prompt or '`' in optimized_prompt:
                    logging.warning(f"提示词包含非法字符，重试 {retry_count + 1}/{max_retries}")
                    retry_count += 1
                    # 更新系统提示，强调不要包含特殊字符
                    data["messages"][0]["content"] += " 重要提醒：不要在回复中包含任何大括号{}、中括号[]或反引号`。"
                    continue
                    
                if "prompt" in optimized_prompt.lower():
                    logging.warning(f"提示词包含'prompt'关键词，重试 {retry_count + 1}/{max_retries}")
                    retry_count += 1
                    # 更新系统提示，强调不要包含'prompt'关键词
                    data["messages"][0]["content"] += " 重要提醒：不要在回复中包含'prompt'这个词。"
                    continue
                
                print(f"原始提示词: {prompt}")
                print(f"优化后提示词: {optimized_prompt}")
                
                return optimized_prompt
            
            except Exception as e:
                error_str = str(e)
                # 检查是否为内容过滤错误
                if "content_filter" in error_str:
                    print(f"您生成的内容不符合内容审查的规范，请重新使用合适的提示词")
                    logging.warning(f"您生成的内容不符合内容审查的规范，请重新使用合适的提示词: {prompt}")
                    return prompt
                
                logging.error(f"提示词优化失败 (尝试 {retry_count + 1}/{max_retries}): {error_str}")
                retry_count += 1
                if retry_count >= max_retries:
                    logging.warning(f"达到最大重试次数，返回原始提示词")
                    return prompt
        
        # 如果所有尝试都失败，返回原始提示词
        return prompt


# 为了保持向后兼容性，提供与原始函数相同的接口
async def text2image_from_togetherai_api(prompt: str, 
                                        generate_steps: int = 4, 
                                        output_size_width: int = 1024, 
                                        output_size_height: int = 1024, 
                                        model: str = "black-forest-labs/FLUX.1-schnell-Free",
                                        n: int = 1,
                                        need_optimize_prompt: bool = True):
    generator = ImageGenerator()
    return await generator.text2image(
        prompt=prompt,
        generate_steps=generate_steps,
        output_size_width=output_size_width,
        output_size_height=output_size_height,
        model=model,
        n=n,
        need_optimize_prompt=need_optimize_prompt
    )

async def image2image_from_togetherai_api(
    image_url: str,
    prompt: str = "",
    generate_steps: int = 4,
    output_size_width: int = 1024,
    output_size_height: int = 1024,
    model: str = "black-forest-labs/FLUX.1-schnell-Free",
    n: int = 1,
    strength: float = 0.8,
    need_optimize_prompt: bool = False
):
    generator = ImageGenerator()
    return await generator.image2image(
        image_url=image_url,
        prompt=prompt,
        generate_steps=generate_steps,
        output_size_width=output_size_width,
        output_size_height=output_size_height,
        model=model,
        n=n,
        strength=strength,
        need_optimize_prompt=need_optimize_prompt
    )

def optimize_prompt(prompt):
    generator = ImageGenerator()
    return generator.optimize_prompt(prompt)
