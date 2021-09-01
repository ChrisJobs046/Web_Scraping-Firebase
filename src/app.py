from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from P_Firebase import *


app = FastAPI()

@app.post("/WebScraping/", status_code = status.HTTP_201_CREATED)
def post_data():
    ref.push()
    return {"message": "Hello World"}

@app.get("/WebScraping/", status_code = status.HTTP_200_OK)
def get_data():
    ref.get()
    return {"message": "Hello World"}


""" 
@app.put("/WebScraping/", status_code = status.HTTP_200_OK)
def put_data():
    return {"message": "Hello World"}

@app.delete("/WebScraping/", status_code = status.HTTP_204_NO_CONTENT)
def delete_data(data_title: str):
    return {"message": "Note  with id: {} deleted successfully".format(data_title)}
"""

origins = [

    "http://localhost:3000",
    "http://localhost:8080",
]

app = FastAPI(title="Rest Api using FastApi PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["client-facing-example-app.com", "localhost:5000"],
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


