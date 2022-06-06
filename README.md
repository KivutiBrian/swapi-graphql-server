# swapi-graphql-server
A GraphQL API that wraps the Star Wars API  (https://swapi.dev/). 

## Features

* FastAPI
* Strawberry - To define GraphQL Schema
* JWT token authentication
* CORS (Cross Origin Resource Sharing)


## Installation

1.Clone Repo via http

```
https://github.com/KivutiBrian/swapi-graphql-server.git
```

or via ssh

```
git@github.com:KivutiBrian/swapi-graphql-server.git
```

2.Create Virtual Environment folder

```
python -m venv env
```

3.Activate virtual environment in parent directory of your "env"

For Linux systems and MAC

```
source env/bin/activate
```

For Windows

```
env\Scripts\activate.bat
```

4.Install requierements
```
pip install -r requirements.txt
```

5.Setup environment variables. create a ***.env*** file.
Required basic env variables are
```
ACCESS_TOKEN_EXPIRES_MINUTES
ALGORITHM = HS256
BASE_URL = https://swapi.dev/api/people

```

6. To run the code
```
uvicorn main:app --reload
```

7. To run using docker on local or production
```
docker-compose -f docker-compose.dev.yml up --build
docker-compose -f docker-compose.prod.yml up --build
```

## Important Features to note

This part highlights some importants features to note.


### shema.py
defines our GraphQL schema, queries and mutations


### settings
Includes *** configs.py *** that defines a Setting class that maps .env variables 
