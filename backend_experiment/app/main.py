import fastapi

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request
from fastapi.responses import RedirectResponse, Response, JSONResponse
# from fastapi.security import OAuth2PasswordBearer
from fastapi_cognito import CognitoAuth, CognitoSettings, CognitoToken
from typing import Mapping, Sequence, Optional, Any, List, Dict

import datetime
from jose import jwt
import httpx
import os

from .utils import (
    get_hmac_key,
    get_cognito_jwks,
    verify_jwt,
)

async def get_token_from_cookie(request: Request):
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Access token not found",
        )
    else:
        verification = verify_jwt(access_token, get_cognito_jwks())
        if not verification:
            raise HTTPException(
                status_code=401,
                detail="Invalid access token",
            )
            
    return access_token


app = FastAPI()


@app.get("/")
def root() -> Mapping[str, str]:
    return {"message": "App functioning"}


@app.get("/callback")
async def process_cognito_code(code: str, response: Response):
    data = {
        "grant_type": "authorization_code",
        "client_id": os.environ.get("COGNITO_APP_CLIENT_ID"),
        "client_secret": os.environ.get("COGNITO_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": os.environ.get("COGNITO_REDIRECT_URL"),
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    async with httpx.AsyncClient() as client:
        cognito_response = await client.post(
            os.environ.get("COGNITO_TOKEN_URL"), data=data, headers=headers
        )
        print(cognito_response.json())
    if cognito_response.status_code != 200:
        raise HTTPException(
            status_code=401, detail="Invalid callback code, or some other error"
        )

    # If this succeeded, we have valid ID token, access token, refresh token, and expiry time
    cognito_json = cognito_response.json()
    access_token = cognito_json["access_token"]
    id_token = cognito_json["id_token"]
    refresh_token = cognito_json["refresh_token"]
    expires_in = datetime.datetime.now().timestamp() + int(cognito_json["expires_in"])

    # Extract and decode the ID token to determine the user's identity
    cognito_jwks = get_cognito_jwks()
    # decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
    if not verify_jwt(id_token, cognito_jwks):
        raise HTTPException(status_code=401, detail="Invalid ID token signature")
    decoded_id_token = jwt.decode(
        token=id_token,
        key=get_hmac_key(id_token, cognito_jwks),
        algorithms=["RS256"],
        audience=os.environ.get("COGNITO_APP_CLIENT_ID"),
        access_token=access_token,
    )
    username = decoded_id_token["cognito:username"]
    email = decoded_id_token["email"]
    print(decoded_id_token)

    # Store all tokens in respective cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True,
    )
    response.set_cookie(
        key="id_token", value=id_token, httponly=True, samesite="none", secure=True
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
    )
    response.set_cookie(
        key="expires_at",
        value=str(expires_in),
        httponly=True,
        samesite="none",
        secure=True,
    )

    # Return a success message, or some non-sensitive user info from the ID token.
    return {"message": "Login successful!", "username": email}


@app.get("/redirect")
async def debug_get_endpoint(request: Request) -> Dict[str, Any]:
    params = dict(request.query_params)
    headers = dict(request.headers)
    return {"params": params, "headers": headers}


@app.get("/protected/{id}")
def protected_int(id: int, token: CognitoToken = Depends(get_token_from_cookie)) -> int:
    return id


@app.get("/logout")
async def logout(response: Response):
    domain = os.environ.get("DEPLOYMENT_DOMAIN")
    response = JSONResponse({"message": "Logout successful"})
    response.delete_cookie(key="access_token", domain=domain)
    response.delete_cookie(key="id_token", domain=domain)
    response.delete_cookie(key="refresh_token", domain=domain)
    response.delete_cookie(key="expires_at", domain=domain)
    return response
