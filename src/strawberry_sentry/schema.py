import asyncio
from typing import Any, List

import sentry_sdk
import strawberry
from sqlalchemy import select
from strawberry.dataloader import DataLoader

from strawberry_sentry.db import DbUser, async_session


@strawberry.type
class User:
    id: int
    name: str


@sentry_sdk.trace
async def load_users(keys: list[int]) -> List[User]:
    await asyncio.sleep(2)
    async with async_session() as session:
        users_by_id = {
            u.id: u
            for u in await session.scalars(select(DbUser).where(DbUser.id.in_(keys)))
        }
        return [
            User(id=users_by_id[int(key)].id, name=users_by_id[int(key)].name)
            for key in keys
        ]


async def get_context() -> Any:
    return {"user_loader": DataLoader(load_fn=load_users)}


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, info: strawberry.Info, id: strawberry.ID) -> User:
        return await info.context["user_loader"].load(id)


schema = strawberry.Schema(query=Query)
