# AI Summariser API

A FastAPI app that uses Claude to summarise text and maintain conversations.

## Endpoints

- `POST /summarise` — returns 3-bullet summary of any text
- `POST /chat` — multi-turn conversation with memory
- `GET /docs` — interactive API docs

## Live URL
https://web-production-b6b55.up.railway.app/docs#/default/chat_chat_post -- will probably not be useful in like 10 mins from deployemnt

## Stack
- FastAPI
- Anthropic Claude Haiku
- Railway (deployment)

## Run locally
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
uvicorn main:app --reload