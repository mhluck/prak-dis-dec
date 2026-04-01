from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import schema  # file kamu

app = FastAPI()

graphql_app = GraphQLRouter(schema.schema)
app.include_router(graphql_app, prefix="/graphql")