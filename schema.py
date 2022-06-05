import json
from typing import Optional, List
import strawberry, requests
from datetime import timedelta

# custom imports
from settings.config import settings
from utils.security import create_access_token

@strawberry.type
class Token:
    token_type: str
    access_token: str

@strawberry.type
class User:
    username: str

@strawberry.type
class Person:
    name: str
    height: str
    mass: str
    gender: str
    homeworld: str

def personDetail(personDict):   
    return Person(name=personDict["name"],height=personDict["height"],mass=personDict["mass"],gender=personDict["gender"],homeworld=personDict["homeworld"])

# Queries
@strawberry.type
class Query:

    # TODO : ADD Error handlers
    
    @strawberry.field
    def people(self, page: Optional[int] = 1) -> Optional[List[Person]]:
        if page:
            r = requests.get(f"{settings.BASE_URL}/?page={page}")
            data = r.json()["results"]
            cleaned_data = list(map(personDetail, data))
            return cleaned_data
        
    @strawberry.field
    def person(self, name: str) -> Person:
        if name:
            r = requests.get(f"{settings.BASE_URL}/?search={name}")
            data = r.json()["results"][0]
            return Person(name=data["name"],height=data["height"],mass=data["mass"],gender=data["gender"],homeworld=data["homeworld"])
        
            
        
    

# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    def authenticate(self, username: str) -> Token:
        #access token expires in minutes
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(token_type='bearer', access_token=create_access_token(subject=username, expires_delta=access_token_expires))

schema = strawberry.Schema(query=Query, mutation=Mutation)

