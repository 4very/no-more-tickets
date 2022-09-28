from fastapi.responses import JSONResponse
from pydantic import BaseModel, SecretStr, EmailStr
from json import loads
from requests import HTTPError

from main import HTTPError as HTTPErrorType
from firebase.pyrebase import auth as pauth

from . import router

# REGISTER ACCOUNT
class authRegisterBody(BaseModel):
    email: EmailStr
    password: SecretStr

class authRegisterResponse(BaseModel):
    email: EmailStr
    idToken: str
    refreshToken: str
    localId: str
    expiresIn: int

# POST new account
@router.post('/register', response_model=authRegisterResponse)
async def register(body: authRegisterBody) -> authRegisterResponse | HTTPErrorType:
    try: 
        register_response: dict[str, str | int] = pauth.create_user_with_email_and_password(body.email, body.password.get_secret_value())
        return register_response

    except HTTPError as error:
        error_code: str = loads(error.args[1])['error']['message']

        # account already exists
        if error_code == "EMAIL_EXISTS":
            return JSONResponse(status_code=400,content={
                "msg": "Account already exists!",
                "type": error_code
            })

        # weak password, firebase specifies it must be atleast 6 char long
        if error_code == "WEAK_PASSWORD":
            return JSONResponse(status_code=400,content={
                "msg": "Password is too weak: Password should be atleast 6 characters",
                "type": error_code
            })

        return JSONResponse(status_code=400, content={
            "msg": "Unknown error occured!",
            "type": error_code
        })
