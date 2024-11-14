from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
posts = []


class PostDetail(BaseModel):
    name: str
    email: str


class Post(BaseModel):
    title: str
    description: str
    author: PostDetail


@app.get("/post")
async def post_list():
    return {"posts": posts}


@app.post("/post/create")
async def post_create(post: Post):
    posts.append(post)
    return {"post": post}


@app.get("/post/{post_id}")
async def post_detail(post_id: int):
    try:
        post = posts[post_id - 1]
    except IndexError:
        return {"error": "post not found"}
    return {"post": post}


@app.put("/post/{post_id}")
async def post_update(post_id: int, post: Post):
    posts[post_id - 1] = post
    return {"post": post}
