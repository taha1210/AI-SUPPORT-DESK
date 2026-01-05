import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.agent.graph import build_graph

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_user" 

async def generate_chunks(message: str, thread_id: str):
    """
    This function will retrieve data from agent and yield it in chunks
    """
    agent = build_graph()
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"query": message, "messages": [("user", message)]}

    async for event in agent.astream(inputs, config, stream_mode="values"):
        if "messages" in event:
            last_msg = event["messages"][-1]
            
            if hasattr(last_msg, 'content'):
                content = last_msg.content
            elif isinstance(last_msg, tuple):
                content = last_msg[1]
            else:
                content = str(last_msg)

            yield f"data: {json.dumps({'content': content})}\n\n"
            
            await asyncio.sleep(0.05)

@app.post("/chat")
async def chat(req: ChatRequest):
    return StreamingResponse(
        generate_chunks(req.message, req.thread_id),
        media_type="text/event-stream"
    )