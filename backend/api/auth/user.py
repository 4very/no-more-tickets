from typing import Any
from fastapi.responses import JSONResponse
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError, RevokedIdTokenError, UserDisabledError, CertificateFetchError

from main import HTTPError
from firebase.admin import auth as aauth

from . import router

# USER DATA
# TODO may move this to not auth
# TODO change this to get and figure out where nuxt auth puts the token

# GET user data
@router.get('/user')
async def user(token: str) -> HTTPError | Any:
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

