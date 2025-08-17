from fastapi import FastAPI , status , HTTPException ,Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.security.api_key import APIKeyHeader
import os
from dotenv import load_dotenv
load_dotenv()
from main import run_agent

app = FastAPI()
KEY_NAME = "x-api-key"
API_KEY=os.getenv("API_KEY")
header_api_key = APIKeyHeader(name=KEY_NAME)


def validate_api_key(api_key:str = Security(header_api_key)):
 if api_key == API_KEY:
  return api_key
 else:
  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def check_status():
    return {"status": "ok"}


@app.post("/agentic-search")
async def agentic_search(query:str, api_key: str = Depends(validate_api_key)):
   output = await run_agent(query)
   return {"output":jsonable_encoder(output)}



