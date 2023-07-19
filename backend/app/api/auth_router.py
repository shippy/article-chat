from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
import os
import httpx
import datetime
from jose import jwt
from sqlmodel import Session, select

from app.core.auth import (
    get_cognito_jwks,
    verify_jwt,
    get_hmac_key,
    set_secure_httponly_cookie,
    get_token_from_cookie,
)
from app.models.user import User
from app.core.database import get_session

cognito_router = APIRouter()


@cognito_router.get("/callback")
async def process_cognito_code(
    code: str, response: Response, session: Session = Depends(get_session)
):
    data = {
        "grant_type": "authorization_code",
        "client_id": os.environ.get("COGNITO_APP_CLIENT_ID"),
        "client_secret": os.environ.get("COGNITO_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": os.environ.get("COGNITO_REDIRECT_URL"),
    }
    print(data)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    async with httpx.AsyncClient() as client:
        cognito_response = await client.post(
            f"{os.environ.get('COGNITO_DOMAIN')}/oauth2/token",
            data=data,
            headers=headers,
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

    user = session.exec(select(User).where(User.cognito_id == username)).first()

    if not user:
        user = User(cognito_id=username, username=email)
        session.add(user)
        session.commit()
        session.refresh(user)

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
    return {"message": "Login successful!", "username": user.username}


@cognito_router.get("/logout")
async def logout(response: Response):
    domain = os.environ.get("DEPLOYMENT_DOMAIN")
    response = JSONResponse({"message": "Logout successful"})
    response.delete_cookie(key="access_token", domain=domain)
    response.delete_cookie(key="id_token", domain=domain)
    response.delete_cookie(key="refresh_token", domain=domain)
    response.delete_cookie(key="expires_at", domain=domain)
    return response