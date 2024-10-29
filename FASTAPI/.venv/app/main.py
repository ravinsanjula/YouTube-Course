from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel #This is to validate the data
from typing import Optional
from random import randrange
import pypyodbc


app =FastAPI()



@app.get("/")
def root():
    return {"message": "Hello Sanjula"}

#Title str, content str, category, Boolean (He we allowed user to only give these inpts)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#Connecting to the database
conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=;{DESKTOP-DFE9VSL}'
    r'DATABASE=fastapi;'
    r'Trusted_Connection=yes;'
)
conn = pypyodbc.connect(conn_str)

try:
    conn = pypyodbc.connect(conn_str)
    print("Connection Successfull")
except Exception as error:
    print("connecting to database fail")
    print("Error",error)



my_posts =[{"title":"title of post 1","content":"content of post 1","id":1},
           {"title":"Favorite food","content":"I like pizza","id":2}]

#@app is the method then the path
@app.get("/getpost")
def root():
    return {"data":my_posts}

@app.get("/posts")
def get_post():
    return {"data":"This is your post"}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

def find_post(id):
    for i in my_posts:
        if i['id'] == id:
            return i
def find_index_post(id:int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/posts/latest")
def get_latest():
    post = my_posts[len(my_posts)-1]
    return {"detail":post}

@app.get("/getpost/{id}")
def get_post(id: int,response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
    return {"post_detail":post}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
   
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"item {id} is not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index = find_index_post(id) #find index is a predefined function check above code
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}
    print(post)
    ##for i in my_posts:
        #if i["id"] == id:
            #my_posts[i] == id
        #else:
            #return Response(status_code=status.HTTP_404_NOT_FOUND)




