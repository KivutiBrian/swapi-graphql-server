import json
from typing import Optional, List
import strawberry, requests
from datetime import timedelta

# custom imports
from settings.config import settings
from utils.security import create_access_token, validate_token, LoginSuccess, LoginError

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


# Helper function to convert the personDict into a Person Object
def personDetail(personDict):   
    return Person(name=personDict["name"],height=personDict["height"],mass=personDict["mass"],gender=personDict["gender"],homeworld=personDict["homeworld"])

# Queries
@strawberry.type
class Query:

    # TODO : ADD Error handlers

    @strawberry.field
    def people(self,token:str, page: Optional[int] = 1) -> Optional[List[Person]]:
        
        # validate token passed on the request
        # check if the return type of the function call of validate_token is of LoginError or LoginSuccess
        if isinstance(validate_token(token), LoginError) or isinstance(validate_token(token), LoginSuccess):
            raise Exception("Invalid Token")
        else:
            # check if page has been passed
            if page:
                # make api call to fetch all people
                r = requests.get(f"{settings.BASE_URL}/?page={page}")
                data = r.json()["results"]
                cleaned_data = list(map(personDetail, data))
                return cleaned_data
            else:
                raise Exception("Required page parameter not passed")
        
    @strawberry.field
    def person(self,token: str, name: str) -> Optional[Person]:

        # validate token passed on the request
        # check if the return type of the function call of validate_token is of LoginError or LoginSuccess
        if isinstance(validate_token(token), LoginError) or isinstance(validate_token(token), LoginSuccess):
            raise Exception("Invalid Token")
        else:
            # check name has been passes
            if name:
                # make api call to get person detail by name
                r = requests.get(f"{settings.BASE_URL}/?search={name}")

                # if length of resilt is 0 -> return None
                if len(r.json()["results"]) == 0:
                    return None
                else:
                    data = r.json()["results"][0]
                    return Person(name=data["name"],height=data["height"],mass=data["mass"],gender=data["gender"],homeworld=data["homeworld"])
        

# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    def authenticate(self, username: str) -> Token:
        try:
            #access token expires in minutes
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            return Token(token_type='bearer', access_token=create_access_token(subject=username, expires_delta=access_token_expires))
        except Exception as e:
            raise Exception(e)


schema = strawberry.Schema(query=Query, mutation=Mutation)

