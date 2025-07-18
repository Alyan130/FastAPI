from fastapi import FastAPI, HTTPException ,status
from pydantic import BaseModel
from agent import main


app = FastAPI()

class Response(BaseModel):
    message: str


class UserInput(BaseModel):
    message: str

@app.post("/agent", response_model=Response)
async def agent_endpoint(message: UserInput):
    try:
        prompt = message.model_dump().get("message")
        response = await main(str(prompt))
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    