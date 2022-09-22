from pydantic import BaseModel
from fastapi import APIRouter
router = APIRouter()

@router.get('/login')
async def login():
    return {"message": "Hello World"}

@router.get('/register')
async def register():
    return {"message": "Hello World"}

@router.get('/forgot_password')
async def forgot_password():
    return {"message": "Hello World"}

