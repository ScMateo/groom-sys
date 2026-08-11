from pydantic import BaseModel, Field

class AdminLoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)

class AdminLoginResponse(BaseModel):
    message: str
    authenticated: bool
    username: str