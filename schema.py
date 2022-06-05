import strawberry
from datetime import timedelta

# custom imports
from utils.security import create_access_token
from settings.config import settings

@strawberry.type
class Token:
    token_type: str
    access_token: str


# Queries
@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    def authenticate(self, username: str) -> Token:
        #access token expires in minutes
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(token_type='bearer', access_token=create_access_token(subject=username, expires_delta=access_token_expires))

schema = strawberry.Schema(query=Query, mutation=Mutation)

