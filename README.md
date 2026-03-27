# WhatsApp E-commerce Support Bot

A production-quality WhatsApp customer support bot for e-commerce businesses.
Built with FastAPI, Twilio, GPT-4o-mini, Redis, and SQLite.

## Features

- WhatsApp messaging via Twilio
- GPT-4o-mini powered intelligent replies
- Per-user conversation memory (Redis hot cache + SQLite cold storage)
- Configurable business context via text file
- Input validation and error handling
- Multi-language support (English + Urdu)
- Graceful out-of-scope handling

## Tech stack

| Layer | Tool |
|---|---|
| API server | FastAPI |
| WhatsApp gateway | Twilio |
| LLM | GPT-4o-mini |
| Hot cache | Redis (Memurai on Windows) |
| Persistence | SQLite + SQLAlchemy async |
| Deployment | Railway |

## Project structure
```
app/
  main.py       — FastAPI app, webhook handler, input validation
  config.py     — environment variable loading
  session.py    — Redis + SQLite two-layer session management
  llm.py        — OpenAI async wrapper
  prompt.py     — system prompt builder
  database.py   — SQLite models and queries

data/
  business_info.txt — business context and rules for the bot
```

## Local development

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your keys
3. Run `uv sync`
4. Activate venv: `.venv\Scripts\activate`
5. Start Redis (Memurai on Windows, or Docker)
6. Start server: `uvicorn app.main:app --reload`
7. Start tunnel: `ngrok http 8000`
8. Set Twilio sandbox webhook to: `https://YOUR_NGROK_URL/webhook`

## Environment variables

See `.env.example` for all required variables.

## Test scenarios

| # | Input | Expected |
|---|---|---|
| 1 | hi | Friendly greeting |
| 2 | return policy | 7 day return policy |
| 3 | delivery time | 3-5 business days |
| 4 | payment methods | COD, bank transfer, EasyPaisa |
| 5 | track order SS-10423 | Asks for order number |
| 6 | damaged item | Apologizes, asks for photo |
| 7 | memory test | Remembers name and order |
| 8 | weather today | Out of scope rejection |
| 9 | are you a robot | Says "I am StyleBot" |
| 10 | Urdu message | Replies in Urdu |