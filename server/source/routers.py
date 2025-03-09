from fastapi import APIRouter, HTTPException
from source.models import Text2ImageRequest, Text2ImageResponse
from source.algorithm import ImageGenerator

# 创建路由器
router = APIRouter()
image_generator = ImageGenerator()

# 创建路由
@router.post("/image_generation", response_model=Text2ImageResponse)
async def image_generation(request: dict):
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
        
        # 获取生成图片数量
        n = request.get("count", 1)
        
        image_urls = await image_generator.text2image(prompt=combined_prompt,n=n)
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
