from fastapi import APIRouter, HTTPException, Body
from source.models import Text2ImageRequest, Text2ImageResponse
from source.algorithm import ImageGenerator
from typing import Dict, Any

# 创建路由器
router = APIRouter(tags=["图像生成"])
image_generator = ImageGenerator()

# 创建路由
@router.post("/image_generation", response_model=Text2ImageResponse, summary="文本生成图像", description="根据文本提示词生成图像")
async def image_generation(
    request: Dict[str, Any] = Body(
        ...,
        example={
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
    )
):
    """
    文本生成图像API
    
    - **prompt**: 生成图像的文本提示词
    - **negativePrompt**: 负面提示词，指定不希望出现在图像中的内容
    - **stylePrompt**: 风格提示词，指定图像的艺术风格
    - **colorPrompt**: 颜色提示词，指定图像的色彩偏好
    - **lightPrompt**: 光照提示词，指定图像的光照效果
    - **compositionPrompt**: 构图提示词，指定图像的构图方式
    - **count**: 生成图像的数量
    - **width**: 输出图像宽度
    - **height**: 输出图像高度
    - **model**: 使用的模型名称
    - **needOptimizePrompt**: 是否需要优化提示词
    """
    try:
        # 组合提示词
        combined_prompt = request.get("prompt", "")
        
        # 添加其他提示词
        if request.get("negativePrompt"):
            combined_prompt += f", 避免: {request.get('negativePrompt')}"
        if request.get("stylePrompt"):
            combined_prompt += f", 风格: {request.get('stylePrompt')}"
        if request.get("colorPrompt"):
            combined_prompt += f", 色彩: {request.get('colorPrompt')}"
        if request.get("lightPrompt"):
            combined_prompt += f", 光照: {request.get('lightPrompt')}"
        if request.get("compositionPrompt"):
            combined_prompt += f", 构图: {request.get('compositionPrompt')}"
        # 获取模型选择
        model = request.get("model", None)
        
        # 获取输出尺寸设置
        output_size_width = request.get("width", None)
        output_size_height = request.get("height", None)
        
        # 获取是否需要提示词优化
        need_optimize_prompt = request.get("needOptimizePrompt", True)
        # 获取生成图片数量
        n = request.get("count", 1)
        
        image_urls = await image_generator.text2image(
            prompt=combined_prompt,
            model=model,
            output_size_width=output_size_width,
            output_size_height=output_size_height,
            n=n,
            need_optimize_prompt=need_optimize_prompt
        )
        # # 判断是否有参考图片
        # if request.get("referenceImage"):
        #     # 将base64图像上传到S3并获取URL
        #     import base64
        #     import io
        #     import uuid
            
        #     # 解码base64图像
        #     image_data = base64.b64decode(request.get("referenceImage").split(",")[-1])
            
        #     # 上传到S3
        #     reference_image_url = image_generator._upload_to_s3(image_data, "reference_images")
            
        #     # 调用image2image函数
        #     image_urls = await image_generator.image2image(
        #         image_url=reference_image_url,
        #         prompt=combined_prompt,
        #         n=n
        #     )
        # else:
        #     # 调用text2image函数
        #     image_urls = await image_generator.text2image(
        #         prompt=combined_prompt,
        #         n=n
        #     )
        
        # 构建返回结果
        generated_images = []
        for i, url in enumerate(image_urls):
            import datetime
            generated_images.append({
                "id": i + 1,
                "url": url,
                "title": f"生成图片 {i+1}",
                "createdAt": datetime.datetime.now().isoformat()
            })
        
        # 返回标准响应格式
        return Text2ImageResponse(
            code=200,
            message="图像生成成功",
            data=generated_images
        )
    except Exception as e:
        # 异常处理
        raise HTTPException(status_code=500, detail=f"图像生成失败: {str(e)}")
