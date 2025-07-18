from sqlalchemy import Column ,Integer, String ,ForeignKey
from database import Base
from pydantic import BaseModel , Field

class User(Base):
    __tablename__ = "Users"

    Id = Column(Integer,primary_key=True, index=True ,autoincrement=True)
    username = Column(String(50))  
    password = Column(String(255))


class Products(Base):
    __tablename__ = "Products"
    
    product_id = Column(Integer , primary_key=True, autoincrement=True)
    name = Column(String(50))
    user_id = ForeignKey("Users.Id")  

   