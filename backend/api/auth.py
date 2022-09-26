from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
router = APIRouter()
from firebase.pyrebase import auth as pauth
from requests import HTTPError
from firebase.admin import auth as aauth
from json import loads
from pprint import pprint




class loginBody(BaseModel):
    email: EmailStr
    password: str

class loginResponse(BaseModel):
    localId: str
    email: str
    idToken: str
    refreshToken: str
    expiresIn: int

# POST login 
@router.post('/login', response_model=loginResponse)
async def login(login: loginBody):
    try:
        # use pyrebase to validate the credentials submitted
        user = pauth.sign_in_with_email_and_password(login.email, login.password)
        return user

    except HTTPError as e:
        # get the error message from HTTPError
        error = loads(e.args[1])['error']['message']

        # email not found
        if (error == 'EMAIL_NOT_FOUND'):
            return JSONResponse(status_code=400,content={
                "msg": "No account found with this email!",
                "type": error
            })

        # invalid password
        if (error == 'INVALID_PASSWORD'):
            return JSONResponse(status_code=400, content={
                "msg": "Password is invalid!",
                "type": error
            })
        
        # else
        return JSONResponse(status_code=400, content={
            "msg": "Unknown error occured!",
            "type": "UNKNOWN_ERROR"
        })


# POST new token
@router.post('/refresh')
async def refresh():
    return {"message": "Hello World"}

# POST logout
@router.post('/logout')
async def logout():
    return {"message": "Hello World"}


# POST request for password reset
@router.post('/forgot_password')
async def forgot_password():
    return {"message": "Hello World"}


# POST new account
@router.post('/register')
async def register():
    return {"message": "Hello World"}