from time import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


# Here will bind our models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Setup database connection
while True:
    try:
        # conn = psycopg2.connect(host, database, user, password)
        conn = psycopg2.connect(host='localhost', database='fastapi_db', user='ahmed', password='ahmed@admin123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error", error)
        time.sleep(2)

my_posts = [
    {
        "id": 1,
        "title":"title of post[1]",
        "content": "content of post[2]"
    },
    {
        "id": 2,
        "title":"favorite foods",
        "content": "I like pizza"
    }
    ]

def find_post(id):
    for item in my_posts:
        if item['id'] == id:
            return item
    return None

def find_index_post(id):
    for i, item in enumerate(my_posts):
        if item['id'] == id:
            return i
    return None

# Root - Default
@app.get("/")
def root():
    return {
            "message": "Welcome to my API",
            "name": "Eng. Ahmed Hemdan"
        }

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

# Retrieve Posts
@app.get("/posts")
def get_posts():
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return {"data": posts}

# Create Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    # This approach is safe
    cursor.execute("insert into posts(title, content, published) values (%s, %s, %s) returning* ", (post.title, post.content, post.published))

    new_post = cursor.fetchone()

    conn.commit()

    # This approach is not safe
    # cursor.execute(f"insert into posts(title, content, published) values ({post title}, {post.content}, {post.published})")
    return {"data": new_post}

# Get Post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""select * from posts where id = %s""", (id,))  # <-- Fix here
    returned_post = cursor.fetchone()
    if not returned_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found.")
    return {"data": returned_post}

# Delete Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("delete from posts where id =%s returning *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is not None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found.")

# Update Post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (updated_post.title, updated_post.content, updated_post.published, id)
    )
    updated_post_data = cursor.fetchone()
    conn.commit()
    if updated_post_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found.")
    return {"data": updated_post_data}