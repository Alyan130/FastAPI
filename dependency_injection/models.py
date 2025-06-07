from pydantic import BaseModel , Field 
from typing import Any

class Users(BaseModel):
    uid:int = Field(...,ge=1)
    username:str
    email:str

class ApiResponse(BaseModel):
     status_code:int
     data:Any



