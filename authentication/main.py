from fastapi import FastAPI , Depends ,HTTPException ,status
from database import SessionLocal, engine
from models import Base
from typing import Annotated
from sqlalchemy.orm import Session
import auth
from typing import Annotated, Dict
from auth import get_current_user
import products

app = FastAPI()
app.include_router(auth.router)
app.include_router(products.router)

Base.metadata.create_all(bind=engine)


def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


db_dependancy = Annotated[Session,Depends(get_db)]
user_dependancy = Annotated[Dict,Depends(get_current_user)]

@app.get("/users")
async def get_user(user:user_dependancy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Un authenticated request")
    
    return user


