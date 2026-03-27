from datetime import datetime
from sqlalchemy import String, Text, DateTime, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./chat_history.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_messages(phone: str, user_message: str, bot_reply: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(Message(phone=phone, role="user", content=user_message))
            session.add(Message(phone=phone, role="assistant", content=bot_reply))


async def load_history(phone: str, limit: int = 10) -> list:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Message)
            .where(Message.phone == phone)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        messages = list(reversed(messages))
        return [{"role": m.role, "content": m.content} for m in messages]