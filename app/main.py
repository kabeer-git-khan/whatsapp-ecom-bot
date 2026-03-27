from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from app.config import settings
from app.prompt import build_messages
from app.llm import get_reply

app = FastAPI(title="WhatsApp E-commerce Bot")


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

    messages = build_messages([], user_message)
    reply = await get_reply(messages)

    print(f"[OUT] {phone}: {reply}")

    twiml = MessagingResponse()
    twiml.message(reply)

    return Response(content=str(twiml), media_type="application/xml")