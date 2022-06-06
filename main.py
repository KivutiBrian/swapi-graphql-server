from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

# custom imports
from schema import schema

app = FastAPI(
    contact={
        "name": "Brian Kivuti",
        "email": "briankivuti1@gmail.com"
    }
)
# setup the middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # [str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
app.add_api_websocket_route("/graphql", graphql_app)
