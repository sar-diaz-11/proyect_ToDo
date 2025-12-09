{{ ... }}

class User(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    token: str