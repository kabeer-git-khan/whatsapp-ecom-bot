from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from app.config import settings

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

    print(f"Message from {phone}: {user_message}")

    reply = f"Echo: {user_message}"

    response = MessagingResponse()
    response.message(reply)

    return Response(content=str(response), media_type="application/xml")