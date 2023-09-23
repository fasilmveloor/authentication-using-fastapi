from pydantic import BaseModel
import datetime

class UserCreate(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    is_active: bool
