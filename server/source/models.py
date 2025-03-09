from pydantic import BaseModel
from typing import List, Optional, Dict

# 定义请求模型
class Text2ImageRequest(BaseModel):
    prompt: str
    generate_steps: Optional[int] = 4
    output_size_width: Optional[int] = 1024
    output_size_height: Optional[int] = 1024
    model: Optional[str] = "black-forest-labs/FLUX.1-schnell-Free"
    n: Optional[int] = 1

# 定义响应模型
class Text2ImageResponse(BaseModel):
    code: int = 200
    message: str = "成功"
    data: List[Dict] 