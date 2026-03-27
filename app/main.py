from contextlib import asynccontextmanager

from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from app.config import settings
from app.database import init_db
from app.prompt import build_messages
from app.llm import get_reply
from app.session import get_history, save_turn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("[STARTUP] Database initialized")
    yield
    print("[SHUTDOWN] App shutting down")


app = FastAPI(title="WhatsApp E-commerce Bot", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "bot": "whatsapp-ecom-bot"}


@app.post("/webhook")
async def webhook(
    From: str = Form(...),
    Body: str = Form(...),
):
    phone = From
    user_message = Body.strip()

    print(f"[IN]  {phone}: {user_message}")

    history = await get_history(phone)
    messages = build_messages(history, user_message)
    reply = await get_reply(messages)

    await save_turn(phone, user_message, reply)

    print(f"[OUT] {phone}: {reply}")

    twiml = MessagingResponse()
    twiml.message(reply)

    return Response(content=str(twiml), media_type="application/xml")