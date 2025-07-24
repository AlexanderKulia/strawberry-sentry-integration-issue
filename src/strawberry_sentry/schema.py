import asyncio
from typing import Any, List

import sentry_sdk
import strawberry
from strawberry.dataloader import DataLoader


@strawberry.type
class User:
    id: int


@sentry_sdk.trace
async def load_users(keys: list[int]) -> List[User]:
    await asyncio.sleep(2)
    return [User(id=key) for key in keys]


async def get_context() -> Any:
    return {"user_loader": DataLoader(load_fn=load_users)}


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, info: strawberry.Info, id: strawberry.ID) -> User:
        return await info.context["user_loader"].load(id)


schema = strawberry.Schema(query=Query)
