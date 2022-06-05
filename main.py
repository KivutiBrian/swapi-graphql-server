from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# custom imports
from schema import schema

app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
app.add_api_websocket_route("/graphql", graphql_app)

