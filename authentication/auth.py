from fastapi import APIRouter , HTTPException ,Depends ,status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import SessionLocal
from typing import Annotated
from models import User
from schemas import Token , Users
from passlib.context import CryptContext
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from datetime import timedelta ,datetime

# "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbHlhbiIsImlkIjoiMTIzNDUiLCJleHAiOjE3NTIwNjEwNDJ9.vpXkikK4tfJdpAcTS1ANhBZ8QonKAA6LJ0qAqn5g7nk"

router = APIRouter(prefix="/auth",tags=["auth"])

SECRET_KEY = "EqsauAOResqHEnsxmYjulc0VErOpRZGl"
ALGORITHM = "HS256"

bycrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


db_dependancy = Annotated[Session,Depends(get_db)]


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependancy,user_data:Users):
   create_user_model = User(
       username = user_data.username,
       password = bycrypt_context.hash(user_data.password) 
   )
   db.add(create_user_model)
   db.commit()
   return JSONResponse(
     content={
         "message":"user created!"
     }
   )


@router.post("/token")
async def login_user(form:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependancy):
    user = authenticate_user(form.username,form.password,db)

    if not user:
         HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Error login")
    token = create_jwt_token(form.username, form.password ,timedelta(days=1))

    return JSONResponse(
        content={"access_token":token,"token_type":"Bearer"}
    )

def authenticate_user(username:str,password:str,db):
       user = db.query(User).filter(User.username == username).first()
       if not user:
           return False
       if not bycrypt_context.verify(password,user.password):
          return False
       return user
    
def create_jwt_token(username,u_id,expire_time:timedelta):
        encode = {"sub":username,"id":u_id}
        expires = datetime.utcnow() + expire_time
        encode.update({"exp":expires})
        return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


def get_current_user(token:Annotated[Token,Depends(oauth2_bearer)]):
    decode = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    username = decode.get("sub")
    Id = decode.get("id")

    if not username and not Id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Not authenticated")
    try:
      return JSONResponse(
          content={"username":username,"id":Id}
      )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

