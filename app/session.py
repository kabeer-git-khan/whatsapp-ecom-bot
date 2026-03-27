import json
import redis.asyncio as aioredis
from app.config import settings
from app.database import save_messages, load_history

REDIS_URL = settings.redis_url
SESSION_TTL = 86400

redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)


async def get_history(phone: str) -> list:
    try:
        cached = await redis_client.get(phone)
        if cached:
            print(f"[SESSION] Redis hit for {phone}")
            return json.loads(cached)

        print(f"[SESSION] Redis miss for {phone} — loading from SQLite")
        history = await load_history(phone)

        if history:
            await redis_client.setex(phone, SESSION_TTL, json.dumps(history))

        return history

    except Exception as e:
        print(f"[SESSION] Redis error: {e} — falling back to SQLite")
        return await load_history(phone)


async def save_turn(phone: str, user_message: str, bot_reply: str) -> None:
    await save_messages(phone, user_message, bot_reply)

    try:
        cached = await redis_client.get(phone)
        history = json.loads(cached) if cached else []

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_reply})

        history = history[-10:]

        await redis_client.setex(phone, SESSION_TTL, json.dumps(history))
        print(f"[SESSION] Saved turn for {phone}, history length: {len(history)}")

    except Exception as e:
        print(f"[SESSION] Redis error on save: {e}")