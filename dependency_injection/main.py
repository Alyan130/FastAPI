from fastapi import FastAPI ,HTTPException ,Depends, status
from models import Users , ApiResponse
from data import users_db

app = FastAPI()


def get_user(user_id):
  for user in users_db:
    if user.uid == user_id:
       return user
  else:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User not found"
    )
  
@app.get("/products")
def get_produts(user:Users = Depends(get_user)):
  return ApiResponse(status_code=status.HTTP_200_OK,data=user)


@app.get("/orders")
def get_orders(user:Users =Depends(get_user)):
    return ApiResponse(status_code=status.HTTP_200_OK,data=user)


