from fastapi import FastAPI

from api import auth
from docs.tags import tags_metadata

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class HTTPError(BaseModel):
    msg: str
    type: str




responses = {
    400: {'model': HTTPError}
}

app = FastAPI(openapi_tags=tags_metadata, responses=responses)

origins = [
    "http://localhost",
    "http://localhost:8082",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router, prefix='/auth', tags=['auth'])