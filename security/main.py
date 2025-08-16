from fastapi import FastAPI, HTTPException , status ,Depends , Security , Query
from fastapi.security.api_key import APIKeyHeader
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Annotated , Literal


app = FastAPI(
    title="Secure API",
    description="This is a secure API",
    )

class Techdata(BaseModel):
    frontend:List[str]
    backend:List[str]
    cloud:List[str]

technologies = {
   "frontend":["react","vuejs","angular"],
   "backend":["django","flask","spring"],
   "cloud":["aws","gcp","azure"]
   }

API_KEY = "12e5ghjj75"
KEY_NAME = "x-api-key"

header_api_key = APIKeyHeader(name=KEY_NAME)

def validate_api_key(api_key:str = Security(header_api_key)):
 if api_key == API_KEY:
  return api_key
 else:
  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")


@app.get("/")
def root():    
    return {"message": "Hello World"}

@app.get("/data")
def data(api_key:str = Depends(validate_api_key),q = Literal["frontend","backend","cloud"]):
  if q:
    return technologies[q]
  else:
        return technologies
    

@app.post("/create")
def create_technology(api_key:str = Depends(validate_api_key),tech:List[str]):
    technologies.update({"tech":tech})
    return {"message": "Technology created successfully","technologies":technologies}




   