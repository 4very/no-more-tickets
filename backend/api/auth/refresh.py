from fastapi.responses import JSONResponse
from pydantic import BaseModel, SecretStr, EmailStr
from http.client import HTTPException
from json import loads
from requests import HTTPError

from main import HTTPError as HTTPErrorType
from firebase.admin import auth as aauth
from firebase.pyrebase import auth as pauth

from . import router

# REFRESH DATA
class authRefreshBody(BaseModel):
    refreshToken: str
    userId: str


class authRefreshResponse(BaseModel):
    userId: str
    idToken: str
    refreshToken: str


# POST new token
@router.post("/refresh", response_model=authRefreshResponse)
async def refresh(body: authRefreshBody) -> authRefreshResponse | HTTPErrorType:
    try:
        refresh_response: dict[str, str | int] = pauth.refresh(body.refreshToken)

        # extra verification check
        if refresh_response["userId"] != body.userId:
            return JSONResponse(
                status_code=400,
                content={
                    "msg": "Response UserId doesn't specified UserId",
                    "type": "USERID_MISMATCH",
                },
            )
        return refresh_response

    except HTTPError as error:
        error_code: str = loads(error.args[1])["error"]["message"]

        # refresh token isnt valid
        if error_code == "INVALID_REFRESH_TOKEN":
            return JSONResponse(
                status_code=400,
                content={"msg": "Refresh token is invalid!", "type": error_code},
            )

        # else
        return JSONResponse(
            status_code=400,
            content={"msg": "Unknown error occured!", "type": error_code},
        )
