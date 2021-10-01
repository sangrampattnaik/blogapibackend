from pydantic import BaseModel


class Status(BaseModel):
    message: str


class BlogIn(BaseModel):
    title: str
    body: str
    base64_image_encoded: str
    
    class Config:
        orm_mode = True
        schema_extra = {"example": {"title": "blog title", "body": "blog body","base64_image_encoded":"Normal Base64 String"}}