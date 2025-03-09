from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# 定义请求模型
class Text2ImageRequest(BaseModel):
    prompt: str = Field(
        description="生成图像的文本提示词",
        example="一只可爱的猫咪在草地上玩耍"
    )
    generate_steps: Optional[int] = Field(
        default=4,
        description="生成步数，值越大生成质量越高但耗时更长",
        example=4
    )
    output_size_width: Optional[int] = Field(
        default=1024,
        description="输出图像宽度",
        example=1024
    )
    output_size_height: Optional[int] = Field(
        default=1024,
        description="输出图像高度",
        example=1024
    )
    model: Optional[str] = Field(
        default="black-forest-labs/FLUX.1-schnell-Free",
        description="使用的模型名称",
        example="black-forest-labs/FLUX.1-schnell-Free"
    )
    n: Optional[int] = Field(
        default=1,
        description="生成图像的数量",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "一只可爱的猫咪在草地上玩耍",
                "generate_steps": 4,
                "output_size_width": 1024,
                "output_size_height": 1024,
                "model": "black-forest-labs/FLUX.1-schnell-Free",
                "n": 1
            }
        }

# 定义响应模型
class Text2ImageResponse(BaseModel):
    code: int = Field(default=200, description="状态码", example=200)
    message: str = Field(default="成功", description="状态信息", example="图像生成成功")
    data: List[Dict] = Field(
        description="生成的图像信息列表",
        example=[
            {
                "id": "img_123456",
                "title": "猫咪图像",
                "url": "https://example.com/images/cat.png",
                "createdAt": "2023-03-09T12:34:56Z"
            }
        ]
    ) 