# Sentry integration for Strawberry

`SENTRY_DSN` environment variable is required for the Sentry integration to work

```sh
poetry install
poetry run uvicorn strawberry_sentry.app:app
```

When `getUser` query is executed, trace gets sent to Sentry, but it is missing the `graphql.query` span that includes `graphql.parse`, `graphql.validate` and `graphql.resolve` spans
