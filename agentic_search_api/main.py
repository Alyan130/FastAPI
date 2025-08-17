from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,exceptions,RunContextWrapper
from agents import set_default_openai_key,function_tool
import asyncio
from pydantic import BaseModel
from agents.mcp import MCPServerStreamableHttp, MCPServerStdio,MCPServerSse,MCPServer, MCPServerSseParams
from openai.types.responses import ResponseTextDeltaEvent
from agents.mcp import MCPServerStreamableHttp , MCPServerStreamableHttpParams
from agents import SQLiteSession
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)
DAPPIER_KEY = os.getenv("DAPPIER_KEY")
API_KEY= os.getenv("GEMINI_KEY")

external_client = AsyncOpenAI(
    api_key = API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
      model="gemini-2.0-flash",
      openai_client= external_client
)

session = SQLiteSession("123")

mcp_params  = MCPServerSseParams(
    url = f"https://mcp.dappier.com/sse?apiKey={DAPPIER_KEY}",                                          
    )

async def run_agent(query:str):
 async with MCPServerSse(
    params=mcp_params,
    cache_tools_list=True,
    client_session_timeout_seconds=50) as server:
      try:
         agent = Agent(
             name = "Search Agent",
             instructions = '''
             - You are knowledge base agent you have access to dappier mcp server, you can use these tools to search for information.
             - Use dappier tools to search for information , summarize it and provde short information.
             ''',
             model = model,
             mcp_servers=[server],
         )
         print(f"server started!")
         result =await Runner.run(agent,query,session=session)
         return result.final_output
      except Exception as e:
         print(f"Error occured {e}")


if __name__ == "__main__":
   asyncio.run(run_agent("web"))
