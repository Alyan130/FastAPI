from pydantic import BaseModel, Field

class Users(BaseModel):
   username:str 
   password:str


class Token(BaseModel):
    access_token:str
    token_type:str

class Product(BaseModel):
    name:str
