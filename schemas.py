from pydantic import BaseModel,Field

class User(BaseModel):
    username: str = Field(min_length=3,max_length=12)
    password: str = Field(min_length=8)

class RefreshRequest(BaseModel):
    refresh_token: str