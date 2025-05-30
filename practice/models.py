from pydantic import BaseModel , Field
from typing import Literal,Optional ,Any

class Book(BaseModel):
     book_id:int  = Field(...,ge=0 , le=1000)
     title:str = Field(...,min_length=5)
     author:str
     genre:Literal["fiction","astronomy","horror","adventure"]
     year:int


class Review(BaseModel):
     reviewer:str
     rating:int = Field(...,ge=1,le=5)
     comment: Optional[str] = None


class ApiResponse(BaseModel):
    status_code:int
    data:Optional[Any]


