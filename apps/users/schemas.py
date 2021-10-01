from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {"example": {"username": "username", "password": "password"}}


class UserLoginOutSchema(BaseModel):
    status: str = "success"
    message: str = "login successfull"
    token: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwidHlwZSI6IkJlYXJlciIsImV4cCI6MTYzMjkzNjE4Nn0.j8fcvhhier5J8ypvzoUMsa7MszSSc7KCy95__Ssmfn8"
