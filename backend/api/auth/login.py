from fastapi.responses import JSONResponse
from pydantic import BaseModel, SecretStr, EmailStr
from http.client import HTTPException
from json import loads
from requests import HTTPError

from main import HTTPError as HTTPErrorType
from firebase.admin import auth as aauth
from firebase.pyrebase import auth as pauth

from . import router

class authLoginBody(BaseModel):
    email: EmailStr
    password: SecretStr

class authLoginResponse(BaseModel):
    localId: str
    email: EmailStr
    idToken: str
    refreshToken: str
    expiresIn: int

# POST login 
@router.post('/login', response_model=authLoginResponse)
async def login(login: authLoginBody) -> authLoginResponse | HTTPErrorType:
    try:
        # use pyrebase to validate the credentials submitted
        user = pauth.sign_in_with_email_and_password(login.email, login.password.get_secret_value())
        return user

    except HTTPError as error:
        # get the error message from HTTPError
        error_code: str = loads(error.args[1])['error']['message']

        # email not found
        if (error_code == 'EMAIL_NOT_FOUND'):
            return JSONResponse(status_code=400,content={
                "msg": "No account found with this email!",
                "type": error_code
            })

        # invalid password
        if (error_code == 'INVALID_PASSWORD'):
            return JSONResponse(status_code=400, content={
                "msg": "Password is invalid!",
                "type": error_code
            })

        if (error_code == 'USER_DISABLED'):
            return JSONResponse(status_code=400, content={
                "msg": "User's account is disabled!",
                "type": error_code
            })

        # else
        return JSONResponse(status_code=400, content={
            "msg": "Unknown error occured!",
            "type": error_code
        })


