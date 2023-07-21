from fastapi import Depends, HTTPException, Response, Request
from fastapi_cognito import CognitoAuth, CognitoSettings
from app.core.settings import settings
from app.core.database import get_session
from app.models.user import User

from jose import jwt, jwk
from jose.utils import base64url_decode
import os
import re
from typing import Any, Dict, List, Literal, Mapping, Optional
from pydantic import BaseModel
import requests
from functools import lru_cache
from sqlmodel import Session, select

cognito_eu = CognitoAuth(settings=CognitoSettings.from_global_settings(settings))
if "localhost" not in os.environ.get("DEPLOYMENT_DOMAIN", ""):
    CROSS_SITE_SCRIPTING_COOKIE = re.sub(
        r"(https?://)?api\.", ".", os.environ.get("DEPLOYMENT_DOMAIN", "")
    )
else:
    CROSS_SITE_SCRIPTING_COOKIE = None

# https://gntrm.medium.com/jwt-authentication-with-fastapi-and-aws-cognito-1333f7f2729e

JWK = Dict[str, str]


class JWKS(BaseModel):
    keys: List[JWK]


class JWTAuthorizationCredentials(BaseModel):
    jwt_token: str
    header: Dict[str, str]
    claims: Dict[str, str]
    signature: str
    message: str


@lru_cache()
def get_cognito_jwks() -> JWKS:
    return JWKS(
        **requests.get(
            f"https://cognito-idp.{os.environ.get('COGNITO_REGION')}.amazonaws.com/"
            f"{os.environ.get('COGNITO_POOL_ID')}/.well-known/jwks.json"
        ).json()
    )


def get_hmac_key(token: str, jwks: JWKS) -> Optional[JWK]:
    kid = jwt.get_unverified_header(token).get("kid")
    for key in jwks.keys:
        if key.get("kid") == kid:
            return key


def verify_jwt(token: str, jwks: JWKS) -> bool:
    hmac_key = get_hmac_key(token, jwks)

    if not hmac_key:
        raise ValueError("No public key found!")

    hmac_key = jwk.construct(hmac_key)

    message, encoded_signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode())

    return hmac_key.verify(message.encode(), decoded_signature)


async def verify_and_decode_token(
    token: str, access_token: Optional[str] = None
) -> Mapping[str, Any]:
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token not found",
        )
    else:
        jwks = get_cognito_jwks()
        verification = verify_jwt(token, jwks)
        if not verification:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        hmac_key = get_hmac_key(token, jwks)

        if not hmac_key:
            raise ValueError("No matching public key found!")

        try:
            decoded_token = jwt.decode(
                token,
                hmac_key,
                algorithms=["RS256"],
                audience=os.environ.get("COGNITO_APP_CLIENT_ID"),
                access_token=access_token,
            )
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"Error decoding token: {e}",
            )

    return decoded_token


async def verify_and_decode_access_token_from_request(
    request: Request,
) -> Mapping[str, Any]:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="No access token found",
        )
    return await verify_and_decode_token(access_token)


def set_secure_httponly_cookie(
    response: Response,
    key: str,
    value: Any,
    samesite: Literal["lax", "strict", "none"] = "lax",
    domain: Optional[str] = CROSS_SITE_SCRIPTING_COOKIE,
) -> None:
    # print(f"Setting {key} cookie to {value} for {domain}")
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=True,
        samesite=samesite,
        domain=domain,
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


async def get_current_user(
    session: Session = Depends(get_session),
    token=Depends(verify_and_decode_access_token_from_request),
) -> User:
    user = session.exec(
        select(User).where(User.cognito_id == token.get("username"))
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
