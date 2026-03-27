from contextlib import asynccontextmanager

from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from app.database import init_db
from app.prompt import build_messages
from app.llm import get_reply
from app.session import get_history, save_turn

MAX_MESSAGE_LENGTH = 500


def make_twiml(text: str) -> Response:
    twiml = MessagingResponse()
    twiml.message(text)
    return Response(content=str(twiml), media_type="application/xml")


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
    Body: str = Form(""),
):
    phone = From
    user_message = Body.strip()

    print(f"[IN]  {phone}: {user_message}")

    if not user_message:
        print("[SKIP] Empty message received")
        return make_twiml("Sorry, I did not receive any text. Please type your question.")

    if len(user_message) > MAX_MESSAGE_LENGTH:
        print(f"[SKIP] Message too long: {len(user_message)} chars")
        return make_twiml("Your message is too long. Please keep it under 500 characters.")

    try:
        history = await get_history(phone)
        messages = build_messages(history, user_message)
        reply = await get_reply(messages)
        await save_turn(phone, user_message, reply)

    except Exception as e:
        print(f"[ERROR] {e}")
        reply = "Sorry, I am having trouble right now. Please try again in a moment."

    print(f"[OUT] {phone}: {reply}")

    return make_twiml(reply)