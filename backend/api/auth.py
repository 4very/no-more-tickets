from http.client import HTTPException
from typing import Any
from pydantic import BaseModel, EmailStr, SecretStr
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from firebase.pyrebase import auth as pauth
from requests import HTTPError
from firebase.admin import auth as aauth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError, RevokedIdTokenError, UserDisabledError, CertificateFetchError


from json import loads

from pprint import pprint

router = APIRouter()


# LOGIN DATA
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
async def login(login: authLoginBody) -> authLoginResponse | HTTPError:
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

# USER DATA
# TODO may move this to not auth
# TODO change this to get and figure out where nuxt auth puts the token

# GET user data
@router.get('/user')
async def user(token: str):
    # verify token with firebase
    try: 
        response = aauth.verify_id_token(token, check_revoked=True)
        # TODO: get user information
        return response

    # if token isnt a string or a blank string
    # firebase_admin already does this error checking so we can just leverage that
    except ValueError:
        return JSONResponse(status_code=400,content={
                "msg": "Invalid token",
                "type": "INVALID_TOKEN"
            })

    # token is expired and needs to be refreshed
    except ExpiredIdTokenError:
        return JSONResponse(status_code=400,content={
                "msg": "Expired token",
                "type": "EXPIRED_TOKEN"
            })

    # token has been revoked
    except RevokedIdTokenError:
        return JSONResponse(status_code=400,content={
                "msg": "Revoked token",
                "type": "REVOKED_TOKEN"
            })

    # else for revoked and expired, includes malformed or other bad statuses
    except InvalidIdTokenError:
        return JSONResponse(status_code=400,content={
                "msg": "Malformed token",
                "type": "BAD_TOKEN"
            })

    except CertificateFetchError:
        return JSONResponse(status_code=400,content={
                "msg": "Failed to fetch public key certificate required to verify token",
                "type": "CANT_FETCH_CERT"
            })

    # user's account has been disabled
    except UserDisabledError:
        return JSONResponse(status_code=400,content={
                "msg": "User disabled",
                "type": "USER_DISABLED"
            })




# REFRESH DATA
class authRefreshBody(BaseModel):
    refreshToken: str
    userId: str

class authRefreshResponse(BaseModel):
    userId: str
    idToken: str
    refreshToken: str

# POST new token
@router.post('/refresh', response_model=authRefreshResponse)
async def refresh(body: authRefreshBody) -> authLoginResponse | HTTPError:
    try: 
        refresh_response: dict[str, Any] = pauth.refresh(body.refreshToken)

        # extra verification check
        if refresh_response['userId'] != body.userId: 
            return JSONResponse(status_code=400,content={
                "msg": "Response UserId doesn't specified UserId",
                "type": "USERID_MISMATCH"
            })
        return refresh_response

    except HTTPError as error:
        error_code: str = loads(error.args[1])['error']['message']

        # refresh token isnt valid
        if (error_code == 'INVALID_REFRESH_TOKEN'):
            return JSONResponse(status_code=400,content={
                "msg": "Refresh token is invalid!",
                "type": error_code
            })

        # else
        return JSONResponse(status_code=400, content={
            "msg": "Unknown error occured!",
            "type": error_code
        })



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