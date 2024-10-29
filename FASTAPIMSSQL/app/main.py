from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel #This is to validate the data
from typing import Optional
from random import randrange
import  pypyodbc as pyodbc
from main import GlobalException

app =FastAPI()


#Title str, content str, category, Boolean (He we allowed user to only give these inpts)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#Connecting to the database
try:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-DFE9VSL;DATABASE=fastapi')
    cursor = conn.cursor()
    print("Connection Successfull")

except Exception as error:
    print("connecting to database fail")
    print("Error",error)



#Get posts from the database
@app.get("/posts")
def get_post():
    cursor.execute("SELECT * FROM posts")
    post = cursor.fetchall()
    print(post)
    return {"data":post}





