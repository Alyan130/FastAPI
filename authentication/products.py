from fastapi import APIRouter , HTTPException ,Depends ,status
from sqlalchemy.orm import Session
from typing import Annotated, Dict
from auth import get_current_user
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import Product
from models import Products


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


db_dependancy = Annotated[Session,Depends(get_db)]
user_dependancy = Annotated[Dict,Depends(get_current_user)]

router.post("/")
async def create_product(user:user_dependancy,p_name:Product,db:db_dependancy):
    Id = user.get("id")
    create_product_model = Products(
       name=p_name.name,
       user_id = Id
   )
    db.add(create_product_model)
    db.commit()
    return {"message":"user created"}
