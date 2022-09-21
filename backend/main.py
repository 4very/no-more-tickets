from fastapi import FastAPI

import api.auth as auth

app: FastAPI = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)