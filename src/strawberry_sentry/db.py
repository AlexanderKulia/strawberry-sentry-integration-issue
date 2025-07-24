import asyncio

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(AsyncAttrs, DeclarativeBase, MappedAsDataclass):
    pass


class DbUser(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]


engine = create_async_engine("sqlite+aiosqlite:///db.db")
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        session.add_all([DbUser(name="a"), DbUser(name="b")])
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
