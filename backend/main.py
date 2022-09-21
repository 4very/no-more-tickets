from fastapi import FastAPI
import pyrebase

import firebase.firebase as fb






app: FastAPI = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}