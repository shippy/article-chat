import fastapi

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request
from fastapi.responses import RedirectResponse
from fastapi_cognito import CognitoAuth, CognitoSettings, CognitoToken
from typing import Mapping, Sequence, Optional, Any, List, Dict

app = FastAPI()


@app.get("/")
def root() -> Mapping[str, str]:
    return {"message": "App functioning"}


@app.post("/callback")
async def debug_post_endpoint(request: Request) -> Dict[str, Any]:
    body = await request.json()
    headers = dict(request.headers)
    return {"body": body, "headers": headers}


@app.get("/redirect")
async def debug_get_endpoint(request: Request) -> Dict[str, Any]:
    params = dict(request.query_params)
    headers = dict(request.headers)
    return {"params": params, "headers": headers}
