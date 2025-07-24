import os

import dotenv
import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.strawberry import StrawberryIntegration
from strawberry.fastapi import GraphQLRouter

from strawberry_sentry.schema import get_context, schema

dotenv.load_dotenv()
sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    sample_rate=1,
    traces_sample_rate=1,
    integrations=[StrawberryIntegration(async_execution=True)],
)

app = FastAPI()
graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
