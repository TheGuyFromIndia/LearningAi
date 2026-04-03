from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
from typing import List
import asyncio

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
app = FastAPI()
client = anthropic.AsyncAnthropic(api_key=api_key)

class SummariseRequest(BaseModel):
    text: str

class SummariseResponse(BaseModel):
    summary: str
    character_count: int

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    reply: str
    total_messages: int

@app.get("/")
def root():
    return {"status": "alive"}

@app.post("/summarise", response_model=SummariseResponse)
async def summarise(request: SummariseRequest):
    if len(request.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Text too short to summarise")

    try:
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system="You are a concise summariser. Return exactly 3 bullet points. No intro, no outro.",
            messages=[{"role": "user", "content": f"Summarise this:\n\n{request.text}"}]
        )
        summary = message.content[0].text
        return SummariseResponse(
            summary=summary,
            character_count=len(request.text)
        )

    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limited — try again shortly")
    except anthropic.APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"API error: {e.status_code}")
    
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Messages list cannot be empty")

    try:
        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system="You are a helpful assistant.",
            messages=[{"role": m.role, "content": m.content} for m in request.messages]
        )
        return ChatResponse(
            reply=message.content[0].text,
            total_messages=len(request.messages)
        )

    except anthropic.APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"API error: {e.status_code}")