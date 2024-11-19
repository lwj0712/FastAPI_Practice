from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: str
    username: str
    email: str
    password: str


users = []


@app.post(
    "/user/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude={"password"},
)
async def create_user(user: User):
    users.append(user)
    return user


@app.get("/user/")
async def read_user():
    return users
