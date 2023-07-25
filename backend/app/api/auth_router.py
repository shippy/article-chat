from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
import os
import httpx
import datetime
from jose import jwt
from sqlmodel import Session, select

from app.core.auth import (
    exchange_cognito_token_for_credentials,
    get_cognito_jwks,
    get_current_user,
    get_hmac_key,
    set_secure_httponly_cookie,
    verify_jwt,
    CROSS_SITE_SCRIPTING_COOKIE,
)
from app.models.user import User
from app.core.database import get_session

cognito_router = APIRouter()


@cognito_router.get("/callback")
async def process_cognito_code(
    code: str, response: Response, session: Session = Depends(get_session)
):
    # If this succeeded, we have valid ID token, access token, refresh token, and expiry time
    cognito_json = await exchange_cognito_token_for_credentials("authorization_code", code)
    
    # TODO: Refactor the code below this point and use it for refresh token exchange as well
    access_token = cognito_json["access_token"]
    id_token = cognito_json["id_token"]
    refresh_token = cognito_json["refresh_token"]
    expires_in = datetime.datetime.now().timestamp() + int(cognito_json["expires_in"])

    # Extract and decode the ID token to determine the user's identity
    cognito_jwks = get_cognito_jwks()
    decode_key = get_hmac_key(id_token, cognito_jwks)
    if not decode_key:
        raise HTTPException(status_code=401, detail="Irretrievable Cognito public key")
    # decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
    if not verify_jwt(id_token, cognito_jwks):
        raise HTTPException(status_code=401, detail="Invalid ID token signature")
    decoded_id_token = jwt.decode(
        token=id_token,
        key=decode_key,
        algorithms=["RS256"],
        audience=os.environ.get("COGNITO_APP_CLIENT_ID"),
        access_token=access_token,
    )
    username = decoded_id_token["cognito:username"]
    email = decoded_id_token["email"]

    user = session.exec(select(User).where(User.cognito_id == username)).first()

    if not user:
        user = User(cognito_id=username, username=email)
        session.add(user)
        session.commit()
        session.refresh(user)

    response = RedirectResponse(url=f"{os.environ.get('FRONTEND_DOMAIN')}/start")
    # Store all tokens in respective cookies
    set_secure_httponly_cookie(response, "access_token", access_token)
    set_secure_httponly_cookie(response, "id_token", id_token)
    set_secure_httponly_cookie(response, "refresh_token", refresh_token)

    return response


@cognito_router.get("/is_authenticated")
async def is_authenticated(current_user: User = Depends(get_current_user)):
    return JSONResponse(
        {"is_authenticated": True, "user": current_user.username}
    )


@cognito_router.get("/logout")
async def logout(response: Response):
    domain = os.environ.get("DEPLOYMENT_DOMAIN")
    response = RedirectResponse(url=f"{os.environ.get('FRONTEND_DOMAIN')}/")
    response.delete_cookie(key="access_token", domain=CROSS_SITE_SCRIPTING_COOKIE)
    response.delete_cookie(key="id_token", domain=CROSS_SITE_SCRIPTING_COOKIE)
    response.delete_cookie(key="refresh_token", domain=CROSS_SITE_SCRIPTING_COOKIE)
    return response
