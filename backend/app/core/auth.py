from fastapi_cognito import CognitoAuth, CognitoSettings
from .settings import settings

from jose import jwt, jwk
from jose.utils import base64url_decode
import os
from typing import Dict, List, Optional
from pydantic import BaseModel
import requests
from functools import lru_cache

cognito_eu = CognitoAuth(settings=CognitoSettings.from_global_settings(settings))

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
